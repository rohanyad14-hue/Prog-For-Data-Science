"""Notes M1: NLTK pipeline steps and text vectorisation."""
import nltk
from nltk import FreqDist, bigrams, pos_tag
from nltk.corpus import stopwords, wordnet
from nltk.stem import LancasterStemmer, PorterStemmer, WordNetLemmatizer
from nltk.tokenize import sent_tokenize, word_tokenize
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

for pkg, path in [("punkt_tab", "tokenizers/punkt_tab"), ("stopwords", "corpora/stopwords"),
                  ("wordnet", "corpora/wordnet"), ("averaged_perceptron_tagger_eng", "taggers/averaged_perceptron_tagger_eng")]:
    try:
        nltk.data.find(path)
    except LookupError:
        nltk.download(pkg, quiet=True)

text = "Students are studying data science. Dr. Rao's class isn't easy, but the geese in the garden were running faster!"
print("--- tokenization ---")
print("sentences:", sent_tokenize(text))
toks = word_tokenize(text)
print("words    :", toks)
print("note: \"isn't\" -> 'is', \"n't\" and \"Rao's\" -> 'Rao', \"'s\"; punctuation becomes tokens")

print("\n--- cleaning: lower-case, keep alphabetic, remove stopwords ---")
sw = set(stopwords.words("english"))
print("English stopword list size:", len(sw), "| 'not' in list:", "not" in sw, "(removing it can flip sentiment)")
clean = [t.lower() for t in toks if t.isalpha() and t.lower() not in sw]
print(clean)

print("\n--- stemming vs lemmatization ---")
ps, ls, wl = PorterStemmer(), LancasterStemmer(), WordNetLemmatizer()
rows = [("studies", None), ("studying", "v"), ("geese", None), ("running", "v"), ("better", "a"), ("faster", "a"), ("was", "v")]
print(f"{'word':<10}{'Porter':<10}{'Lancaster':<11}{'Lemma (default n)':<19}{'Lemma (with POS)'}")
for w, pos in rows:
    print(f"{w:<10}{ps.stem(w):<10}{ls.stem(w):<11}{wl.lemmatize(w):<19}{wl.lemmatize(w, pos) if pos else '-'}")

print("\n--- POS tagging ---")
tags = pos_tag(word_tokenize("The students are studying data science quickly"))
print(tags)
def wn_pos(tag):
    return {"J": wordnet.ADJ, "V": wordnet.VERB, "N": wordnet.NOUN, "R": wordnet.ADV}.get(tag[0], wordnet.NOUN)
print("POS-aware lemmas:", [wl.lemmatize(w.lower(), wn_pos(t)) for w, t in tags])

print("\n--- frequency, bigrams ---")
doc = word_tokenize("data science needs data and data needs cleaning and science needs data".lower())
print("FreqDist:", FreqDist(doc).most_common(3))
print("bigrams :", list(bigrams(doc))[:4], "...")

print("\n--- bag of words and TF-IDF ---")
docs = ["data science is fun", "science needs data", "fun fun fun games"]
cv = CountVectorizer()
X = cv.fit_transform(docs)
print("vocabulary:", list(cv.get_feature_names_out()))
print("BoW counts:\n", X.toarray())
tf = TfidfVectorizer()
T = tf.fit_transform(docs)
print("TF-IDF (rounded):\n", T.toarray().round(2))
print("idf per word:", dict(zip(tf.get_feature_names_out(), tf.idf_.round(2))))
print("words found in only one document (games, is, needs) get the highest idf; words found in two documents get less.")
