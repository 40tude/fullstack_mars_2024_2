# lit la liste des hotels dans hotels_list.json
# genère un fichier hotels_attributes avec une ligne d'attirbuts par hotel

import json
from pathlib import Path
import logging
import scrapy
from scrapy.crawler import CrawlerProcess

import include_kayak as k
k_CurrentDir     = Path(__file__).parent



# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
class OneHotelSpider(scrapy.Spider):
    name = "OneHotelSpider"
    # make the url are parsed in order
    # however we loose the // ant it is sloooow 
    # 1 min to get the attributs for 25 hotels
    # custom_settings = {
    #   'CONCURRENT_REQUESTS': '1' 
    # }

    def start_requests(self):

      try:
        with open(k_CurrentDir/k.AssetsDir/k.HotelsListFile, 'r') as f:
          data = json.load(f)
      except FileNotFoundError:
        print(f'Are you sure the file {k.HotelsListFile} exists ?')

      hotel_rank = 0
      for entry in data:
        yield scrapy.Request(url=entry['url'], callback=self.parse, meta={"rank": hotel_rank})
        hotel_rank += 1
        


    def parse(self, response):
      
      # get back the rank of the hotel
      rank = response.meta.get("rank")

      # TODO this guys need a review. Indeed, I'm not these hard coded selectors will survive a long time
      # TODO At least they work fine 07/04/2024 
      kScoreSelector          = '.a3b8729ab1.d86cee9b25::text'
      # kDescription1Selector = 'property_description_content::text'                            # <div id="property_description_content" ...
      kDescription2Selector   = '.a53cbfa6de.b3efd73f69::text'                                  # <p data-testid="property-description" class="a53cbfa6de b3efd73f69">....
      klatlng                 = "div.hotel-sidebar-map hotel-sidebar-map-a11y a::attr(href)"    # <div class="hotel-sidebar-map hotel-sidebar-map-a11y">....

      score = response.css(kScoreSelector).get().replace(",", ".")  
      
      url = response.css("div.hotel-sidebar-map a::attr(data-atlas-latlng)").extract()
      latitude = url[0].split(",")[0]
      longitude = url[0].split(",")[1]
      # print(latitude, longitude)

      description = response.css(kDescription2Selector).get()

      processed_data = {
        "rank"        : rank,
        "score"       : score,
        
        "latitude"    : latitude,
        "longitude"   : longitude,
        "description" : description,
      }
      yield processed_data


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# If files exist, delete them 
if Path.exists(k_CurrentDir/k.AssetsDir/k.HotelsAttributes):
  (k_CurrentDir/k.AssetsDir/k.HotelsAttributes).unlink()
if Path.exists(k_CurrentDir/k.AssetsDir/k.ScrapyLogFile):
  (k_CurrentDir/k.AssetsDir/k.ScrapyLogFile).unlink()

process = CrawlerProcess(
    settings={
        "USER_AGENT": "Chrome/97.0",
        "LOG_LEVEL": logging.INFO,  # CRITICAL, ERROR, WARNING, INFO, DEBUG...
        "FEEDS": {
          k_CurrentDir/k.AssetsDir/k.HotelsAttributes: {"format": "json"},  
        },
        "LOG_STDOUT": False,
        "LOG_FILE": f"{k_CurrentDir}/{k.AssetsDir}/{k.ScrapyLogFile}",
    }
)




# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
if __name__ == "__main__":

  process.crawl(OneHotelSpider)
  process.start()


