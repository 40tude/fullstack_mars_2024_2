# lit un fichier one_city.json avec un seul nom de ville
# tient compte des dates de debut et de fin de séjour
# genère un fichier hotels_list.json pour la ville en question

import json
from pathlib import Path
import logging
import scrapy
from scrapy.crawler import CrawlerProcess
from datetime import datetime, timedelta


# kCitiesFile     = "cities.csv"
kOneCityFile    = "one_city.json"
kLogfile        = "scrapy.log"
kOutFile        = "hotels_list.json"
kAssetsDir      = "assets"
kCurrentDir     = Path(__file__).parent
kInHowManyDays  = 15
kLenStay        = 3


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
def build_url(city_str):

  # typiquement
  # checkin  = today + 15 jours
  # checkout = today + 15 jours + 3 jours
  aujourdhui = datetime.today()
  checkin = aujourdhui + timedelta(days=kInHowManyDays)
  checkin_str = checkin.strftime('%Y-%m-%d')

  checkout = checkin + timedelta(days=kLenStay)
  checkout_str = checkout.strftime('%Y-%m-%d')

  return f"https://www.booking.com/searchresults.fr.html?ss={city_str}&checkin={checkin_str}&checkout={checkout_str}&group_adults=2&no_rooms=1&group_children=0"


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
class HotelsListSpider(scrapy.Spider):
  name = "HotelsListSpider"

  
  def start_requests(self):

    try:
      with open(kCurrentDir/kAssetsDir/kOneCityFile, 'r') as f:
        data = json.load(f)
    except FileNotFoundError:
      print(f"Are you sure the file {kOneCityFile} exists ?")
    
    # Not yet usefull but we never know...
    # As today, it creates a list of url with only one url 
    urls = []
    for entry in data:
      cityname = entry['city']
      url = build_url(cityname)
      urls.append(url)
    
    for url in urls:
      yield scrapy.Request(url=url, callback=self.parse)



  def parse(self, response):
    # TODO this guys need a review. Indeed, I'm not these hard coded selectors will survive a long time
    # TODO At least they work fine 07/04/2024 
    kH3HotelSelector  = '.aab71f8e4e'
    kNameSelector     = '.f6431b446c.a15b38c233::text'
    kUrlSelector      = '.a78ca197d0::attr(href)'

    counter = 0  
    for hotel in response.css(kH3HotelSelector):
      
      counter +=1
      if counter == 21:
        break

      hotel_name = hotel.css(kNameSelector).extract_first()
      url = hotel.css(kUrlSelector).get().split("?")[0]

      processed_data = {
        "hotel" : hotel_name,
        "url"   : url,
      }
      yield processed_data
    



# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# If files exist, delete them 
if Path.exists(kCurrentDir/kAssetsDir/kOutFile):
  (kCurrentDir/kAssetsDir/kOutFile).unlink()
if Path.exists(kCurrentDir/kAssetsDir/kLogfile):
  (kCurrentDir/kAssetsDir/kLogfile).unlink()

process = CrawlerProcess(
    settings={
        "USER_AGENT": "Chrome/97.0",
        "LOG_LEVEL": logging.INFO,  # CRITICAL, ERROR, WARNING, INFO, DEBUG...
        "FEEDS": {
          kCurrentDir/kAssetsDir/kOutFile: {"format": "json"},  
        },
        "LOG_STDOUT": False,
        "LOG_FILE": f"{kCurrentDir}/{kAssetsDir}/{kLogfile}",
    }
)

process.crawl(HotelsListSpider)
process.start()
