# Voir https://app.jedha.co/course/web-scraping-ft/become-a-movie-director-ft


# Create a new script called imdb2.py where you'll scrape the same information for all the movies in the chart!


from pathlib import Path
import logging
import scrapy
from scrapy.crawler import CrawlerProcess


# Create a first spider called imdb_spider with:
# name imdb
# start_urls https://www.imdb.com/chart/boxoffice
class IMDBSpider(scrapy.Spider):
    name = "imdb"

    # Url to start your spider from
    start_urls = [
        "https://www.imdb.com/chart/boxoffice",
    ]

    # Callback function that will be called when starting your spider
    # It will get text, author and tags of the first <div> with class="quote"
    def parse(self, response):
        movies = response.xpath(
            "/html/body/div[2]/main/div/div[3]/section/div/div[2]/div/ul/li"
        )  # voir qu'il n'y a pas de '/' à la fin
        for movie in movies:  # TODO prêter attention à la boucle
            yield {
                "ranking": movie.xpath("div[2]/div/div/div/a/h3/text()").get().split(".")[0],
                "title": movie.xpath("div[2]/div/div/div/a/h3/text()").get().split(".")[1].strip(" "),
                "url": movie.xpath("div[2]/div/div/div/a").attrib["href"],"total_earnings": movie.xpath("div[2]/div/div/ul/li[2]/span[2]/text()").get(),                 
                "rating": movie.xpath("div[2]/div/div/span/div/span/text()").get(),
                "nb_voters": movie.xpath("div[2]/div/div/span/div/span/span/text()").getall()[1],
            }



# Name of the file where the results will be saved
filename = "imdb2.json"
current_dir = Path(__file__).parent

# If file already exists, delete it before crawling (because Scrapy will
# concatenate the last and new results otherwise)
# if filename in os.listdir("./"):
#     os.remove("./" + filename)
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
        "LOG_LEVEL": logging.INFO,
        "FEEDS": {
            str(current_dir) + "/" + filename: {"format": "json"},
        },
        # log dans fichier
        "LOG_STDOUT": False,
        "LOG_FILE": f"{current_dir}/scrapy.log",
    }
)


# Start the crawling using the spider you defined above
process.crawl(IMDBSpider)
process.start()
