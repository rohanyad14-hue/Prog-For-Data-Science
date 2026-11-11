"""Sample answer M2-Q3 (collection with Scrapy): one spider per website.
Local copies of the two pages are used (file:// URLs), so no website is contacted."""
import json
import os
import tempfile
from pathlib import Path

import pandas as pd
import scrapy
from scrapy.crawler import CrawlerProcess

os.chdir(tempfile.mkdtemp(prefix="sa_scrapy_"))
Path("site1.html").write_text("""<html><body>
<div class="book" data-id="B101"><h3>Python Basics</h3><span class="price">Rs. 450</span></div>
<div class="book" data-id="B102"><h3>Data Science</h3><span class="price">Rs. 700</span></div>
<div class="book" data-id="B103"><h3>AI Fundamentals</h3><span class="price">Rs. 850</span></div>
</body></html>""", encoding="utf-8")
Path("site2.html").write_text("""<ul>
<li data-id="B101"><span class="rating">4.5</span></li>
<li data-id="B102"><span class="rating">4.8</span></li>
<li data-id="B103"><span class="rating">4.2</span></li>
</ul>""", encoding="utf-8")

POLITE = {"LOG_LEVEL": "ERROR", "ROBOTSTXT_OBEY": True,        # respect robots.txt
          "DOWNLOAD_DELAY": 1, "AUTOTHROTTLE_ENABLED": True}   # be polite to the server


class PriceSpider(scrapy.Spider):                              # website 1: id, title, price
    name = "prices"
    start_urls = [Path("site1.html").resolve().as_uri()]       # in real life: the URL of website 1
    custom_settings = {**POLITE, "FEEDS": {"prices.json": {"format": "json", "overwrite": True}}}

    def parse(self, response):
        for d in response.css("div.book"):
            yield {"BookID": d.attrib["data-id"], "Title": d.css("h3::text").get(),
                   "Price": float(d.css("span.price::text").get().replace("Rs.", "").strip())}


class RatingSpider(scrapy.Spider):                             # website 2: id, rating
    name = "ratings"
    start_urls = [Path("site2.html").resolve().as_uri()]       # in real life: the URL of website 2
    custom_settings = {**POLITE, "FEEDS": {"ratings.json": {"format": "json", "overwrite": True}}}

    def parse(self, response):
        for li in response.css("li"):
            yield {"BookID": li.attrib["data-id"], "Rating": float(li.css("span.rating::text").get())}


process = CrawlerProcess()
process.crawl(PriceSpider)
process.crawl(RatingSpider)
process.start()                                                # runs both spiders, returns when both are done

prices = pd.DataFrame(json.loads(Path("prices.json").read_text(encoding="utf-8")))
ratings = pd.DataFrame(json.loads(Path("ratings.json").read_text(encoding="utf-8")))
print("items collected:", len(prices), "prices and", len(ratings), "ratings")
print(prices.merge(ratings, on="BookID", validate="one_to_one"))
