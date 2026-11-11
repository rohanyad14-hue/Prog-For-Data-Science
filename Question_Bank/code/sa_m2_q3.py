"""Sample answer M2-Q3: collect two tables with Beautiful Soup, clean and merge them with pandas, rank the books by value."""
import pandas as pd
from bs4 import BeautifulSoup

# Stand-ins for the HTML that requests.get(url).text would return from the two websites.
SITE1 = """<html><body>
<div class="book" data-id="B101"><h3>Python Basics</h3><span class="price">Rs. 450</span></div>
<div class="book" data-id="B102"><h3>Data Science</h3><span class="price">Rs. 700</span></div>
<div class="book" data-id="B103"><h3>AI Fundamentals</h3><span class="price">Rs. 850</span></div>
</body></html>"""
SITE2 = """<ul>
<li data-id=" b101 "><span class="rating">4.5</span></li>
<li data-id="B102"><span class="rating">4.8</span></li>
<li data-id="B103"><span class="rating">4.2</span></li>
</ul>"""


def scrape_prices(html):
    soup = BeautifulSoup(html, "html.parser")
    return pd.DataFrame([{"BookID": d["data-id"], "Title": d.h3.text, "Price": d.find("span", class_="price").text}
                         for d in soup.find_all("div", class_="book")])


def scrape_ratings(html):
    soup = BeautifulSoup(html, "html.parser")
    return pd.DataFrame([{"BookID": li["data-id"], "Rating": li.find("span", class_="rating").text} for li in soup.find_all("li")])


def clean(df):
    df = df.copy()
    df["BookID"] = df["BookID"].str.strip().str.upper()                    # keys must match exactly before a merge
    for col in ("Price", "Rating"):
        if col in df:                                  # take the first number in the text; "N/A" and None become NaN
            df[col] = pd.to_numeric(df[col].astype(str).str.extract(r"(\d+(?:\.\d+)?)")[0], errors="coerce")
    return df.drop_duplicates(subset="BookID")


print("--- scraped (raw) ---")
a, b = scrape_prices(SITE1), scrape_ratings(SITE2)
print(a, "\n", b, sep="")
print("keys equal before cleaning:", set(a["BookID"]) == set(b["BookID"]))

print("\n--- cleaned and merged ---")
a, b = clean(a), clean(b)
books = a.merge(b, on="BookID", how="left", validate="one_to_one", indicator=True)
print(books)
print(books["_merge"].value_counts().to_dict())

print("\n--- when the data is messy (missing price, duplicate, missing rating, unmatched id) ---")
dirty_a = pd.DataFrame({"BookID": ["B101", "B102", "B102", "B104"], "Price": ["Rs. 450", "700", "700", "N/A"]})
dirty_b = pd.DataFrame({"BookID": ["b101 ", "B102", "B105"], "Rating": ["4.5", None, "3.9"]})
m = clean(dirty_a).merge(clean(dirty_b), on="BookID", how="outer", indicator=True)
print(m)
print("rows with a missing value:", m[["Price", "Rating"]].isna().any(axis=1).sum(), "| only in one source:", (m["_merge"] != "both").sum())
usable = m.dropna(subset=["Price", "Rating"])
print("usable rows:", usable["BookID"].tolist())

print("\n--- which books are the most valuable? it depends on the definition ---")
minmax = lambda s: (s - s.min()) / (s.max() - s.min())
books["rating_per_100_rs"] = (books["Rating"] / books["Price"] * 100).round(3)
books["weighted_score"] = (0.6 * minmax(books["Rating"]) + 0.4 * (1 - minmax(books["Price"]))).round(3)
print(books[["BookID", "Title", "Price", "Rating", "rating_per_100_rs", "weighted_score"]])
print("best value for money :", books.loc[books["rating_per_100_rs"].idxmax(), "Title"])
print("best weighted score  :", books.loc[books["weighted_score"].idxmax(), "Title"])
print("highest rated        :", books.loc[books["Rating"].idxmax(), "Title"])
