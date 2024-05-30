# AUTHENTIFICATION





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


class QuotesLogin(scrapy.Spider):
    # Name of your spider
    name = "login"

    # Starting URL
    start_urls = ["http://quotes.toscrape.com/login"]

    # Parse function for login
    def parse(self, response):
        # FormRequest used to login
        return scrapy.FormRequest.from_response(
            response,
            formdata={"username": "john", "password": "secret"},
            # Function to be called once logged in
            callback=self.after_login,  # TODO voir le after_login
        )

    # Callback used after login
    def after_login(self, response):
        # Text de la quote en /html/body/div/div[2]/div[1]/div[1]/span[1]
        # On remonte en /html/body/div/div[2]/div[1]/div

        quotes = response.xpath("/html/body/div/div[2]/div[1]/div")
        for quote in quotes:
            yield {
                # /html/body/div/div[2]/div[1]/div[1]/span[1]
                "text": quote.xpath("span[1]/text()").get(),
                # /html/body/div/div[2]/div[1]/div[1]/span[2]/small
                "author": quote.xpath("span[2]/small/text()").get(),
                # /html/body/div/div[2]/div[1]/div[1]/div/a
                "tags": quote.xpath("div/a/text()").getall(),
            }
        # Select the NEXT button and store it in next_page
        try:
            next_page = response.xpath(
                '/html/body/div/div[2]/div[1]/nav/ul/li[@class="next"]/a'
            ).attrib["href"]
        except KeyError:
            # In the last page, there won't be any "href" and a KeyError will be raised
            logging.info("No next page. Terminating crawling process.")
        else:
            # If a next page is found, execute the parse method once again
            yield response.follow(next_page, callback=self.after_login)


# Name of the file where the results will be saved
filename = "4_quotesauthentication.json"
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
process.crawl(QuotesLogin)
process.start()
