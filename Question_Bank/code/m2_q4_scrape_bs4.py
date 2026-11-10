"""M2-Q4a  Scrape a page with Beautiful Soup and store CSV + JSON (Lab experiment 5).
The HTML is embedded so the script runs offline; with a live site you would
replace `html` by requests.get(url, timeout=10).text.
"""
import csv
import json

from bs4 import BeautifulSoup

html = """
<html><body>
  <div class="book"><h2>Python Basics</h2><span class="price">Rs. 450</span><a href="/b/1">details</a></div>
  <div class="book"><h2>Data Science 101</h2><span class="price">Rs. 700</span><a href="/b/2">details</a></div>
  <div class="book"><h2>Scala in Depth</h2><span class="price">Rs. 820</span><a href="/b/3">details</a></div>
</body></html>
"""
with open("books.html", "w", encoding="utf-8") as f:       # reused by the Scrapy example
    f.write(html)

soup = BeautifulSoup(html, "html.parser")
rows = []
for div in soup.find_all("div", class_="book"):
    rows.append({
        "title": div.h2.get_text(strip=True),
        "price": int(div.select_one("span.price").get_text().replace("Rs.", "").strip()),
        "link": div.a["href"],
    })

with open("books_bs4.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["title", "price", "link"])
    w.writeheader()
    w.writerows(rows)
with open("books_bs4.json", "w", encoding="utf-8") as f:
    json.dump(rows, f, indent=2)

print("Parsed", len(rows), "books")
print(open("books_bs4.csv", encoding="utf-8").read())
print("Average price:", sum(r["price"] for r in rows) / len(rows))
