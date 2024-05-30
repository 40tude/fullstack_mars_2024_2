# https://app.jedha.co/course/web-scraping-ft/scraping-yelp-ft


# Create a class YelpSpider(scrapy.Spider)
# with start_urls = ['https://www.yelp.fr/'].
#
# In this class, define a parse(self, response) method that automatically fills Yelp's homepage form with :
#     "restaurant japonais" as search keywords
#     "Paris" as search location.
#
# Then, define another method after_search(self, response) that parses the first page of results, and yields the name and url of each search result.
# Finally, declare a CrawlerProcess that will store the results in a file named "restaurant_japonais-paris.json".

from pathlib import Path
import logging
import scrapy
from scrapy.crawler import CrawlerProcess


class YelpSpider(scrapy.Spider):
    name = "randomquote"
    start_urls = [
        "https://www.yelp.fr",
    ]

    def parse(self, response):
        # return {
        #     "riri": response.xpath(
        #         "/html/body/div/div[2]/div[1]/div/span[1]/text()"  # En dehors de text() on peut mettre quoi ?
        #     ).get(),
        #     "fifi": response.xpath(
        #         "/html/body/div/div[2]/div[1]/div/span[2]/small/text()"
        #     ).get(),
        #     "loulou": response.xpath(
        #         "/html/body/div/div[2]/div[1]/div/div/a/text()"
        #     ).getall(),
        #     # difference entre get() et getall()
        #     # .get() always returns a single result
        #     #     if there are several matches, content of a first match is returned;
        #     #     if there are no matches, None is returned.
        #     # .getall() returns a list with all results.
        # }
        # FormRequest used to login
        return scrapy.FormRequest.from_response(
            response,
            formdata={"find_desc": "restaurant japonais", "search_location": "Paris"},
            # Function to be called once logged in
            callback=self.after_login,           # TODO voir le after_login
        )
    
    # Callback used after login
    def after_login(self, response):
        # Attention les 2 premiers //*[@id="main-content"]/div/ul/li[1] et /li[2] n'ont rien de visible
        # 1er H3 de restau /html/body/yelp-react-root/div[1]/div[5]/div/div/div[1]/main/div/ul/li[3]/div[1]/div/div[2]/div[1]/div[1]/div[1]/div/div/h3/a
        # 2nd H3 de restau //*[@id="main-content"]/div/ul/li[4]/div[1]/div/div[2]/div[1]/div[1]/div[1]/div/div/h3/a
        # quotes = response.xpath("/html/body/div/div[2]/div[1]/div")

        # 
        quotes = response.xpath('//*[@id="main-content"]/div/ul')
        for quote in quotes:
            yield {
                "name": quote.xpath("//*[@id="main-content"]/div/ul/li[3]/div[1]/div/div[2]/div[1]/div[1]/div[1]/div/div/h3/a/text()").get(),
                "url" : quote.xpath("//*[@id="main-content"]/div/ul/li[3]/div[1]/div/div[2]/div[1]/div[1]/div[1]/div/div/h3/a/text()").get(),
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



filename = "restaurant_japonais-paris.json"
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

process.crawl(YelpSpider)
process.start()
