# MULTIPLE ITEMS PER PAGE



# Import os => Library used to easily manipulate operating systems
## More info => https://docs.python.org/3/library/os.html
# import os
from pathlib import Path

# Import logging => Library used for logs manipulation
## More info => https://docs.python.org/3/library/logging.html
import logging

# Import scrapy and scrapy.crawler
import scrapy
from scrapy.crawler import CrawlerProcess


class QuotesSpider(scrapy.Spider):

    # Name of your spider
    name = "quotes"

    # Url to start your spider from
    start_urls = [
        "http://quotes.toscrape.com/page/1/",
    ]

    # Callback function that will be called when starting your spider
    # It will get text, author and tags of all the <div> with class="quote"

    # /html/body/div/div[2]/div[1]/div[1]/span[1]       premiere citation
    # /html/body/div/div[2]/div[1]/div[2]/span[1]       seconde citation

    # /html/body/div/div[2]/div[1]/div[1]     /span[1]  premiere citation
    # /html/body/div/div[2]/div[1]/div[2]     /span[1]  seconde citation

    # /html/body/div/div[2]/div[1]/div        /span[1]  premiere citation
    # /html/body/div/div[2]/div[1]/div        /span[1]  seconde citation
    def parse(self, response):
        quotes = response.xpath(
            "/html/body/div/div[2]/div[1]/div"
        )  # voir qu'il n'y a pas de '/' à la fin
        for quote in quotes:  # TODO prêter attention à la boucle
            # ! yield
            yield {
                "text": quote.xpath(
                    "span[1]/text()"
                ).get(),  # voir qu'il n'y a pas de '/' au début
                "author": quote.xpath("span[2]/small/text()").get(),
                "tags": quote.xpath("div/a/text()").getall(),
            }


# Name of the file where the results will be saved
filename = "2_quotes_alt.json"
current_dir = Path(__file__).parent

# If file already exists, delete it before crawling (because Scrapy will
# concatenate the last and new results otherwise)
# if filename in os.listdir('src/'):
#         os.remove('src/' + filename)
if Path.exists(current_dir / filename):
    (current_dir / filename).unlink()

# Declare a new CrawlerProcess with some settings
## USER_AGENT => Simulates a browser on an OS
## LOG_LEVEL => Minimal Level of Log
## FEEDS => Where the file will be stored
## More info on built-in settings => https://docs.scrapy.org/en/latest/topics/settings.html?highlight=settings#settings
process = CrawlerProcess(
    settings={
        "USER_AGENT": "Chrome/97.0",
        "LOG_LEVEL": logging.INFO,  # CRITICAL, ERROR, WARNING, INFO, DEBUG...
        "FEEDS": {
            str(current_dir) + "/" + filename: {"format": "json"},
        },
    }
)

# Start the crawling using the spider you defined above
process.crawl(QuotesSpider)
process.start()
