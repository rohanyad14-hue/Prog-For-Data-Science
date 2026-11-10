"""Scorecard, mock paper, study resources and the verification appendix."""
from dsl import *
from reportlab.platypus import PageBreak, Paragraph, Table, TableStyle, Spacer

from front import totals
from render import S, Heading, fmt, render_blocks, table_flowable, TEXT_W, NAVY, RULE
from reportlab.lib import colors

MCQ_PICKS = {1: [1, 2, 3, 4], 2: [1, 2, 3, 4], 3: [1, 2, 3, 4], 4: [1, 2, 3, 4], 5: [1, 2], 6: [1, 2]}      # 20 x 1 = 20
SHORT_PICKS = [(1, 1), (1, 5), (2, 3), (2, 6), (3, 1), (3, 6), (4, 6), (4, 7), (5, 1), (6, 3)]                # 10 x 3 = 30
LONG_PICKS = [(1, 2), (2, 2), (3, 4), (4, 4), (5, 2)]                                                       # 5 x 10 = 50


def back_matter(mods, code_dir, out_dir):
    by_num = {m["num"]: m for m in mods}
    fl = [PageBreak(), Heading("Self-scorecard", S["h1"], 0)]
    fl.append(Paragraph(fmt("Write the marks you scored after checking your answers. Aim for at least 60 percent in every module before the exam; "
                            "redo the questions you missed after one day and one week."), S["body"]))
    rows = []
    for m in mods:
        a, b, c, total = totals(m)
        sm = sum(q["marks"] for q in m["shorts"])
        lm = sum(q["marks"] for q in m["longs"])
        rows.append([f"{m['num']}: {m['title']}", f"/ {a}", f"/ {sm}", f"/ {lm}", f"/ {total}", "", ""])
    grand = sum(totals(m)[3] for m in mods)
    rows.append(["<b>Total</b>", "", "", "", f"/ {grand}", "", ""])
    fl += table_flowable(["Module", "MCQ", "Short", "Long", "All", "My score", "%"], rows, [0.36, 0.09, 0.1, 0.1, 0.1, 0.13, 0.12])
    fl.append(Spacer(1, 6))

    # ------------------------------------------------------------------ mock paper
    fl += [Heading("Mock paper (100 marks, 3 hours)", S["h1"], 0)]
    fl.append(Paragraph(fmt("This paper samples every module using questions from the book. It is my own format, not the official pattern; "
                            "adjust it once you have seen a past paper. Attempt it closed-book, then check against the module answers."), S["body"]))
    fl.append(Paragraph("Part A: multiple choice (20 questions, 1 mark each)", S["h3"]))
    k = 1
    for n, idxs in MCQ_PICKS.items():
        m = by_num[n]
        for i in idxs:
            q = m["mcqs"][i - 1]
            opts = "   ".join(f"({'abcd'[j]}) {o}" for j, o in enumerate(q["opts"]))
            fl.append(Paragraph(f"<b>{k}.</b> [M{n}-A{i}] " + fmt(q["q"]) + "<br/>" + fmt(opts), S["bul"]))
            k += 1
    fl.append(Paragraph("Part B: short answers (10 questions, 3 marks each)", S["h3"]))
    for k, (n, i) in enumerate(SHORT_PICKS, 21):
        q = by_num[n]["shorts"][i - 1]
        fl.append(Paragraph(f"<b>{k}.</b> [M{n}-B{i}] " + fmt(q["q"]) + f" <font color='#666666'>({q['marks']} marks)</font>", S["bul"]))
    fl.append(Paragraph("Part C: long questions (5 questions, 10 marks each; full statements are in Part 1 of the module)", S["h3"]))
    for k, (n, i) in enumerate(LONG_PICKS, 31):
        q = by_num[n]["longs"][i - 1]
        fl.append(Paragraph(f"<b>{k}.</b> [M{n}-C{i}] " + fmt(q["title"]) + f" <font color='#666666'>({q['marks']} marks)</font>", S["bul"]))
    check = sum(1 for idxs in MCQ_PICKS.values() for _ in idxs) + sum(by_num[n]["shorts"][i - 1]["marks"] for n, i in SHORT_PICKS) \
        + sum(by_num[n]["longs"][i - 1]["marks"] for n, i in LONG_PICKS)
    assert check == 100, check

    # ------------------------------------------------------------------ resources
    fl += [PageBreak(), Heading("Study material", S["h1"], 0)]
    fl += render_blocks([
        P("Each link below returned HTTP 200 when checked on 7 November 2026. Official documentation comes first because it is the most reliable "
          "and its terms match what examiners use."),
        H3("1. Books already in your folder, mapped to modules"),
        P("Open the PDFs in <i>Prog For Data Science/books</i>. Chapter and page numbers below were read from each file's contents list."),
        T(["Module", "Book (file in your folder)", "Read"], [
            ["1", "<i>Python for Data Analysis</i> (Python-for-Data-Analysis.pdf)", "Ch. 3 Built-in data structures, functions and files (p. 65); Ch. 2 language basics (p. 35)"],
            ["2", "<i>Python for Data Analysis</i>", "Ch. 4 NumPy (p. 101); Ch. 5 pandas (p. 141); Ch. 7 cleaning (p. 221); Ch. 8 join, combine, reshape (p. 265); "
                                                  "Ch. 9 plotting (p. 299); Ch. 10 groupby (p. 337); Ch. 12 modelling libraries (p. 423)"],
            ["2", "<i>Introduction to Machine Learning with Python</i>", "Ch. 3 unsupervised learning and preprocessing: PCA, k-means (p. 145); Ch. 7 text data (p. 337)"],
            ["2", "<i>Become a Python Data Analyst</i> (books/Become-a-Python-Data-AnalystV2B-master.zip)", "the syllabus textbook 1; unzip and read the chapters on pandas and visualisation"],
            ["3, 4", "<i>Data Engineering with Scala and Spark</i> (Packt, 2024)", "Ch. 1 Scala essentials for data engineers (p. 20); Ch. 3 Spark and its APIs (p. 80)"],
            ["4", "<i>Learning Spark</i> (Lightning-Fast Big Data Analysis)", "Ch. 3 programming with RDDs (p. 41); Ch. 7 running on a cluster (p. 135); Ch. 9 Spark SQL (p. 179)"],
            ["4", "<i>Spark in Action</i>", "Ch. 1 introduction (p. 31); Ch. 2 fundamentals (p. 46); Ch. 4 the Spark API in depth (p. 94); Ch. 5 Spark SQL (p. 133)"],
            ["2", "preprints202312.0957.v1.pdf", "a 2023 preprint on supervised machine-learning workflows with numerical and categorical data: background for the modelling part"]],
          [0.08, 0.4, 0.52]),
        NOTE("The Learning Spark and Spark in Action files in your folder look like earlier editions than the ones named in the syllabus (Learning Spark 2nd edition; "
             "Spark in Action 2nd edition): their chapters on DStreams, Mesos and H2O are from the first editions. Concepts are the same, page numbers will not match, and the "
             "newer editions put DataFrames first."),
        H3("2. Official documentation by topic"),
        T(["Topic", "Link"], [
            ["Python data structures, heapq, deque", "https://docs.python.org/3/library/heapq.html   https://docs.python.org/3/library/collections.html"],
            ["Python exceptions", "https://docs.python.org/3/tutorial/errors.html"],
            ["json and csv modules", "https://docs.python.org/3/library/json.html   https://docs.python.org/3/library/csv.html"],
            ["Requests (HTTP)", "https://requests.readthedocs.io/en/latest/"],
            ["NLTK book (tokenizing, stopwords, text)", "https://www.nltk.org/book/ch03.html"],
            ["ChatterBot", "https://docs.chatterbot.us/   https://github.com/gunthercox/ChatterBot"],
            ["NumPy broadcasting", "https://numpy.org/doc/stable/user/basics.broadcasting.html"],
            ["pandas: merge/join/concat, groupby, missing data, text", "https://pandas.pydata.org/docs/user_guide/merging.html   https://pandas.pydata.org/docs/user_guide/groupby.html   "
                                                                       "https://pandas.pydata.org/docs/user_guide/missing_data.html   https://pandas.pydata.org/docs/user_guide/text.html"],
            ["Beautiful Soup, Scrapy", "https://www.crummy.com/software/BeautifulSoup/bs4/doc/   https://docs.scrapy.org/en/latest/intro/overview.html"],
            ["Plotly, Bokeh, Folium", "https://plotly.com/python/   https://docs.bokeh.org/en/latest/   https://python-visualization.github.io/folium/latest/"],
            ["scikit-learn: clustering, PCA", "https://scikit-learn.org/stable/modules/clustering.html   https://scikit-learn.org/stable/modules/decomposition.html"],
            ["Scala 3 book, Scala tour, case classes", "https://docs.scala-lang.org/scala3/book/introduction.html   https://docs.scala-lang.org/tour/tour-of-scala.html   "
                                                       "https://docs.scala-lang.org/overviews/scala-book/case-classes.html"],
            ["Breeze, Saddle, Spire", "https://github.com/scalanlp/breeze   https://saddle.github.io/   https://github.com/typelevel/spire"],
            ["Spark RDD guide, SQL guide, cluster overview", "https://spark.apache.org/docs/latest/rdd-programming-guide.html   https://spark.apache.org/docs/latest/sql-programming-guide.html   "
                                                           "https://spark.apache.org/docs/latest/cluster-overview.html"],
            ["Catalyst optimiser (original article)", "https://www.databricks.com/blog/2015/04/13/deep-dive-into-spark-sqls-catalyst-optimizer.html"],
            ["Class vs case class explained", "https://www.baeldung.com/scala/case-class"],
            ["Choosing a language (syllabus reference 7)", "https://www.aalpha.net/blog/factors-to-consider-when-choosing-a-programming-language/"],
            ["Running Scala without installing it", "https://github.com/VirtusLab/scala-cli"]], [0.3, 0.7]),
        H3("3. Past papers and how your professors set questions"),
        P("I did not find an official VIT marking scheme or a published paper for MACSE502 specifically. These community collections hold VIT CAT and FAT papers for other courses; "
          "check whether this course appears, and if it does, study the question verbs and mark splits."),
        B(["https://papers.codechefvit.com/",
           "https://github.com/CodeChefVIT/papers-codechef",
           "https://github.com/Nirant07/VIT-Papers"]),
        P("The best predictors you already own are the 10 high-frequency FAT questions in your FAT notes (section 6.1), the CAT 2 predicted syllabus file, "
          "and the 20 lab experiments in the syllabus; this book covers all three. Ask seniors or your faculty for the exact FAT pattern and the weight of lab viva."),
    ], code_dir, out_dir)

    # ------------------------------------------------------------------ appendix
    fl += [PageBreak(), Heading("Appendix: how the code was verified", S["h1"], 0)]
    fl += render_blocks([
        T(["File (in Question_Bank/code)", "Runtime", "Notes"], [
            ["m1_q1_placement.py, m1_q2_editor.py, m1_q6_students.py", "Python 3.10", "ran as is; output matches the expected sets, trace and report"],
            ["m1_q3_headlines.py", "Python 3.10, NLTK 3.10.4", "API simulated with a mock session returning real `requests.Response` objects; needs `punkt_tab`, `stopwords`, `wordnet`"],
            ["m1_q4_chatbot.py", "Python 3.10, NLTK, ChatterBot 1.2.15", "ChatterBot ran with `ListTrainer`; needs `python -m spacy download en_core_web_sm`; FAQ data is made up"],
            ["m1_q5_price_alerts.py", "Python 3.10", "mock session (timeout, 429 with Retry-After, 404, invalid JSON); `time.sleep` omitted"],
            ["m2_q1 to m2_q3, m2_q6", "pandas 2.3.3, NumPy 1.26.4, scikit-learn 1.7.2", "ran as is; random values depend on version and seed"],
            ["m2_q4_scrape_bs4.py, m2_q4_scrape_scrapy.py", "Beautiful Soup 4.15, Scrapy 2.19", "page is a local file (`file://` for Scrapy)"],
            ["m2_q5_viz.py", "Plotly 7.1, Bokeh 3.9.2, Folium 0.20", "HTML files were generated and their contents checked for size; not viewed in a browser"],
            ["m3_q1 to m3_q4 (.scala)", "Scala 2.13.12, Java 17, scala-cli", "ran as is"],
            ["m4_q1_exceptions.scala", "Scala 2.13.12", "ran as is"],
            ["m4_q2_breeze.scala", "Breeze 2.1.0, Spire 0.18.0", "ran; two start-up messages from Breeze's native loader omitted in the book"],
            ["m4_q3_saddle.scala", "Saddle 4.0.0-M14 (io.github.pityka fork)", "milestone release; API differs from older Saddle used in your lab file"],
            ["m4_q4_spark.scala", "Spark 3.5.1, `local[2]`", "local mode on one machine; plans and stages are as on a cluster"],
            ["m5_decision_matrix.py", "Python 3.10", "scores are judgements, arithmetic is exact"]], [0.34, 0.26, 0.4]),
        H3("Not verified"),
        B(["Interactive charts (Plotly, Bokeh, Folium) were built but not opened in a browser.",
           "Vegas and Plotly.Scala charts of Labs 18 and 19 were not run; only the Breeze and Saddle parts were.",
           "No live REST service was called; the mock responses reproduce the status codes and bodies described.",
           "Module 6 content is general; the syllabus gives no topics.",
           "Timings (such as NumPy being 38 times faster) are from one machine."]),
        H3("Run it yourself"),
        SNIP("# Python\npip install pandas numpy scikit-learn plotly bokeh folium beautifulsoup4 scrapy nltk requests chatterbot\n"
             "python -m spacy download en_core_web_sm        # needed by ChatterBot 1.2\n"
             "python run_and_capture.py m1_q1_placement.py   # output goes to outputs/\n\n"
             "# Scala (download scala-cli from https://github.com/VirtusLab/scala-cli)\n"
             "scala-cli run code/m3_q2_oop.scala --scala 2.13.12\nscala-cli run code/m4_q4_spark.scala   # downloads Spark on first run", lang="text"),
    ], code_dir, out_dir)
    return fl
