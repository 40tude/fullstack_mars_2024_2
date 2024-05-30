# MULTIPLE PAGES





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


class QuotesMultipleSpider(scrapy.Spider):

    # Name of your spider
    name = "quotesmultiplepages"

    # Url to start your spider from
    start_urls = [
        "http://quotes.toscrape.com/page/1/",
    ]

    # Callback function that will be called when starting your spider
    # It will get text, author and tags of the <div> with class="quote"
    # /html/body/div/div[2]/div[1]/div[1]/span[1]
    def parse(self, response):
        quotes = response.xpath("/html/body/div/div[2]/div[1]/div")
        for quote in quotes:
            yield {
                "text": quote.xpath("span[1]/text()").get(),
                "author": quote.xpath("span[2]/small/text()").get(),
                "tags": quote.xpath("div/a/text()").getall(),
            }

        try:
            # Select the NEXT button and store it in next_page
            # Here we include the class of the li tag in the XPath
            # to avoid the difficujlty with the "previous" button

            # xpath du bouton sur la page 1 = /html/body/div/div[2]/div[1]/nav/ul/li/a
            # on veut pas récupérer le text() on veut le contenu du href
            # sur la page 2 y a un bouton previous en plus du next
            # du coup la première /a c'est celle du bouton previous
            # Dans la page 2 on voit qu'il y a une classe pour le bouton Next
            # previous  => /html/body/div/div[2]/div[1]/nav/ul/li[1]/a
            # next      => /html/body/div/div[2]/div[1]/nav/ul/li[2]/a
            # Voir la difference entre le bouton next de la page 1 (../li/a) et de la page 2 (../li[1]/a)
            next_page = response.xpath(
                '/html/body/div/div[2]/div[1]/nav/ul/li[@class="next"]/a'
            ).attrib["href"]
        except KeyError:
            # ! In the last page, there won't be any "href" and a KeyError will be raised
            # Ca part en vrille à la dernière page MAIS c'est normal
            logging.info("No next page. Terminating crawling process.")
        else:
            # If a next page is found, execute the parse method once again
            yield response.follow(
                next_page, callback=self.parse
            )  # TODO Bien voir le callback=self.parse. Appel recurssif


# Name of the file where the results will be saved
filename = "3_quotesmultiplepages.json"
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
process.crawl(QuotesMultipleSpider)
process.start()
