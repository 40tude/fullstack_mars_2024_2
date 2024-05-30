# FIRST SPIDER

from pathlib import Path
import logging
import scrapy
from scrapy.crawler import CrawlerProcess


class RandomQuoteSpider(scrapy.Spider):
    name = "randomquote"
    start_urls = [
        "http://quotes.toscrape.com/random",
    ]

    def parse(self, response):
        return {
            "riri": response.xpath(
                "/html/body/div/div[2]/div[1]/div/span[1]/text()"  # En dehors de text() on peut mettre quoi ?
            ).get(),
            "fifi": response.xpath(
                "/html/body/div/div[2]/div[1]/div/span[2]/small/text()"
            ).get(),
            "loulou": response.xpath(
                "/html/body/div/div[2]/div[1]/div/div/a/text()"
            ).getall(),
            # difference entre get() et getall()
            # .get() always returns a single result
            #     if there are several matches, content of a first match is returned;
            #     if there are no matches, None is returned.
            # .getall() returns a list with all results.
            # get()
            # [
            #   {"storyline": null}
            # ]
            # 

            # getall()
            # [
            #   {"storyline": []}
            # ]
            
        }







filename = "1_randomquote.json"
current_dir = Path(__file__).parent

# If file already exists, delete it before crawling
# Otherwise Scrapy concatenate the results
if Path.exists(current_dir / filename):
    (current_dir / filename).unlink()

# https://docs.scrapy.org/en/latest/topics/settings.html?highlight=settings#settings
process = CrawlerProcess(
    settings={
        # voir https://www.whatismybrowser.com/guides/the-latest-user-agent/chrome
        # je sais pas encore si tout est utilisable dans scrapy
        "USER_AGENT": "Chrome/97.0",
        "LOG_LEVEL": logging.INFO,  # CRITICAL, ERROR, WARNING, INFO, DEBUG...
        # https://docs.scrapy.org/en/latest/topics/logging.html#topics-logging
        "FEEDS": {
            str(current_dir)
            + "/"
            + filename: {
                "format": "json"
            },  # https://docs.scrapy.org/en/latest/topics/feed-exports.html#std-setting-FEEDS
        },
        # log dans fichier
        "LOG_STDOUT": False,
        "LOG_FILE": f"{current_dir}/scrapy.log",
    }
)

process.crawl(RandomQuoteSpider)
process.start()
