# recoit un nom de ville dans la ligne de commande
# tient compte des dates de debut et de fin de séjour
# genère un fichier hotels_list.json pour la ville en question

import sys
import logging
import scrapy

from pathlib import Path
from scrapy.crawler import CrawlerProcess
from datetime import datetime, timedelta

import include_kayak as k
k_CurrentDir    = Path(__file__).parent
k_CityName      = ""
k_LenStay       = 3
k_InHowManyDays = 15


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
def build_url(city_str):

  # typiquement
  # checkin  = today + 15 jours
  # checkout = today + 15 jours + 3 jours
  aujourdhui = datetime.today()
  checkin = aujourdhui + timedelta(days=k_InHowManyDays)
  checkin_str = checkin.strftime('%Y-%m-%d')

  checkout = checkin + timedelta(days=k_LenStay)
  checkout_str = checkout.strftime('%Y-%m-%d')

  return f"https://www.booking.com/searchresults.fr.html?ss={city_str}&checkin={checkin_str}&checkout={checkout_str}&group_adults=2&no_rooms=1&group_children=0"


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
class HotelsListSpider(scrapy.Spider):
  
  name = "HotelsListSpider"

  
  def start_requests(self):

    # try:
    #   with open(kCurrentDir/kAssetsDir/kOneCityFile, 'r') as f:
    #     data = json.load(f)
    # except FileNotFoundError:
    #   print(f"Are you sure the file {kOneCityFile} exists ?")
    
    # # Not yet usefull but we never know...
    # # As today, it creates a list of url with only one url 
    # urls = []
    # for entry in data:
    #   cityname = entry['city']
    #   url = build_url(cityname)
    #   urls.append(url)
    
    urls = []
    url = build_url(k_CityName)
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
# If files exist, delete them before the CrawlerProcess own it
if Path.exists(k_CurrentDir/k.AssetsDir/k.ScrapyLogFile):
  (k_CurrentDir/k.AssetsDir/k.ScrapyLogFile).unlink()

process = CrawlerProcess(
    settings={
        "USER_AGENT": "Chrome/97.0",
        "LOG_LEVEL": logging.INFO,  # CRITICAL, ERROR, WARNING, INFO, DEBUG...
        "FEEDS": {
          k_CurrentDir/k.AssetsDir/k.HotelsListFile: {"format": "json"},  
        },
        "LOG_STDOUT": False,
        "LOG_FILE": f"{k_CurrentDir}/{k.AssetsDir}/{k.ScrapyLogFile}",
    }
)



# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
if __name__ == "__main__":

  # If files exist, delete it
  if Path.exists(k_CurrentDir/k.AssetsDir/k.HotelsListFile):
    (k_CurrentDir/k.AssetsDir/k.HotelsListFile).unlink()

  if len(sys.argv) == 1:
    # For testing
    k_CityName = "Paris"
  else:  
    k_CityName = sys.argv[1]

  process.crawl(HotelsListSpider)
  process.start()
