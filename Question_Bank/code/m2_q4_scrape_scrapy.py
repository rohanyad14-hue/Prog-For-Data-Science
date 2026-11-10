"""M2-Q4b  The same extraction as a Scrapy spider (runs against the local books.html
through a file:// URL so no website is contacted).
"""
import json
from pathlib import Path

import scrapy
from scrapy.crawler import CrawlerProcess

page = Path("books.html")
if not page.exists():
    raise SystemExit("run m2_q4_scrape_bs4.py first - it writes books.html")


class BookSpider(scrapy.Spider):
    name = "books"
    start_urls = [page.resolve().as_uri()]                 # file:///.../books.html
    custom_settings = {"LOG_LEVEL": "ERROR", "ROBOTSTXT_OBEY": True,
                       "DOWNLOAD_DELAY": 1,               # politeness delay (ignored for file://)
                       "AUTOTHROTTLE_ENABLED": True,
                       "FEEDS": {"books_scrapy.json": {"format": "json", "overwrite": True}}}

    def parse(self, response):
        for div in response.css("div.book"):
            yield {                                        # each yielded dict becomes an item
                "title": div.css("h2::text").get(),
                "price": int(div.css("span.price::text").get().replace("Rs.", "").strip()),
                "link": div.css("a::attr(href)").get(),
            }


process = CrawlerProcess()
process.crawl(BookSpider)
process.start()                                            # blocks until the crawl finishes

items = json.loads(Path("books_scrapy.json").read_text(encoding="utf-8"))
print("Scrapy yielded", len(items), "items")
for it in items:
    print(" ", it)
