from pathlib import Path
import logging
import scrapy
from scrapy.crawler import CrawlerProcess

kCitiesFile = "cities.csv"
kLogfile    = "scrapy.log"
kOutFile    = "hotels_list.json"
kCurrentDir = Path(__file__).parent

class HotelsListSpider(scrapy.Spider):
    name = "HotelsListSpider"
    start_urls = [
      "https://www.booking.com/searchresults.fr.html?ss=Marseille&checkin=2024-05-13&checkout=2024-05-17&group_adults=2&no_rooms=1&group_children=0",
    ]

    # <h3 class="aab71f8e4e">
    # <a href="https://www.booking.com/hotel/fr/suite-en-plein-coeur-du-panier-47-vieux-port.fr.html?aid=304142&amp;label=gen173nr-1FCAQoggJCEHNlYXJjaF9tYXJzZWlsbGVIDVgEaE2IAQGYAQ24ARfIAQzYAQHoAQH4AQOIAgGoAgO4AqyIxLAGwAIB0gIkZDk3MzkzNTItZDcxYS00ZTU4LTkwMWMtMjBmNGE1MDg2Y2U42AIF4AIB&amp;ucfs=1&amp;arphpl=1&amp;checkin=2024-05-13&amp;checkout=2024-05-17&amp;group_adults=2&amp;req_adults=2&amp;no_rooms=1&amp;group_children=0&amp;req_children=0&amp;hpos=1&amp;hapos=1&amp;sr_order=popularity&amp;srpvid=1a9f39d6d8960090&amp;srepoch=1712392466&amp;all_sr_blocks=605171201_389402988_2_0_0&amp;highlighted_blocks=605171201_389402988_2_0_0&amp;matching_block_id=605171201_389402988_2_0_0&amp;sr_pri_blocks=605171201_389402988_2_0_0__35500&amp;from=searchresults#hotelTmpl" 
    # class="a78ca197d0" target="_blank" rel="noopener noreferrer" data-testid="title-link">
    # <div data-testid="title" class="f6431b446c a15b38c233">Suites en plein coeur du Panier et vieux port</div>
    # <div class="ac4a7896c7">Une nouvelle fenêtre va s'ouvrir</div></a>
    # </h3>            

    def parse(self, response):
      kH3HotelSelector  = '.aab71f8e4e'
      kNameSelector     = '.f6431b446c.a15b38c233::text'
      kUrlSelector      = '.a78ca197d0::attr(href)'
        
      for hotel in response.css(kH3HotelSelector):
        hotel_name = hotel.css(kNameSelector).extract_first()
        url = hotel.css(kUrlSelector).get().split("?")[0]
        # url = url.split("?")[0]

        processed_data = {
          "hotel" : hotel_name,
          "url"   : url,
        }
        yield processed_data
      

# If files exist, delete them 
if Path.exists(kCurrentDir/kOutFile):
  (kCurrentDir/kOutFile).unlink()
if Path.exists(kCurrentDir/kLogfile):
  (kCurrentDir/kLogfile).unlink()

process = CrawlerProcess(
    settings={
        "USER_AGENT": "Chrome/97.0",
        "LOG_LEVEL": logging.INFO,  # CRITICAL, ERROR, WARNING, INFO, DEBUG...
        "FEEDS": {
          kCurrentDir/kOutFile: {"format": "json"},  
        },
        "LOG_STDOUT": False,
        "LOG_FILE": f"{kCurrentDir}/{kLogfile}",
    }
)

process.crawl(HotelsListSpider)
process.start()


