# MULTIPLE URLS in //





from pathlib import Path
import logging
import scrapy
from scrapy.crawler import CrawlerProcess

class QuotesSpiderPage(scrapy.Spider):

    name = "quotes"

    # https://stackoverflow.com/questions/71238214/multiple-start-urls-in-python-scrapy-are-running-in-order-or-simultaneously
    # Scrapy is asynchronous in nature.
    # It scrapes the urls in parallel and the order in which requests are enqueued for download is determined by the scheduler
    # https://docs.scrapy.org/en/master/topics/scheduler.html
    start_urls = [
        "http://quotes.toscrape.com/page/1/",
        "http://quotes.toscrape.com/page/2/",
    ]

    def parse(self, response):
        quotes = response.xpath("/html/body/div/div[2]/div[1]/div")
        for quote in quotes:
            yield {
                "text": quote.xpath("span[1]/text()").get(),
                "author": quote.xpath("span[2]/small/text()").get(),
                "tags": quote.xpath("div/a/text()").getall(),
            }


filename = "5_quotesmultiplespiders.json"
current_dir = Path(__file__).parent

if Path.exists(current_dir / filename):
    (current_dir / filename).unlink()

process = CrawlerProcess(
    settings={
        "USER_AGENT": "Chrome/97.0",
        "LOG_LEVEL": logging.INFO,  # CRITICAL, ERROR, WARNING, INFO, DEBUG...
        "FEEDS": {
            str(current_dir) + "/" + filename: {"format": "json"},
        },
    }
)

process.crawl(QuotesSpiderPage)
process.start()
