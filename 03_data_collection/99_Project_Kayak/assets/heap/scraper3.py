from pathlib import Path
import logging
import scrapy
from scrapy.crawler import CrawlerProcess

kCitiesFile = "cities.csv"
kLogfile    = "scrapy.log"
kOutFile    = "kayak.json"
kCurrentDir = Path(__file__).parent

# -----------------------------------------------------------------------------
class HotelsListSpider(scrapy.Spider):
    
    name = "HotelsListSpider"

    start_urls = [
      "https://www.booking.com/searchresults.fr.html?ss=Aix en Provence&checkin=2024-05-02&checkout=2024-05-05&group_adults=2&no_rooms=1&group_children=0",
    ]

    def parse(self, response):
      hotel = response.xpath(
        "/html/body/div[4]/div/div[2]/div/div[2]/div[3]/div[2]/div[2]/div[3]/div[3]/div[1]/div[2]/div/div/div[1]/div/div[1]/div/h3/a/div[1]/text()" 
      ).get()
      # TODO : convertir utf8 en texte ou supporter utf8

      url = response.xpath(
        "/html/body/div[4]/div/div[2]/div/div[2]/div[3]/div[2]/div[2]/div[3]/div[3]/div[1]/div[2]/div/div[1]/div[1]/div/div[1]/div/h3/a"
      ).attrib["href"]

      processed_data = {
        "hotel" : hotel,
        "url" : url,
      }
      yield processed_data



# -----------------------------------------------------------------------------
if __name__ == "__main__":

  # If file exists, delete it 
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


""""
# FIRST SPIDER

from pathlib import Path
import logging
import scrapy
from scrapy.crawler import CrawlerProcess
# import re
import pandas as pd


# import my_api_id as key
# kOpenWeatherMapKey  = key.openweathermap
# kGold               = 1.618
# kWidth              = 12
# kHeight             = kWidth/kGold
# kWidthPx            = 1024
# kHeightPx           = kWidthPx/kGold


class HotelsListSpider(scrapy.Spider):
  def parse(self, response):
    hotel = response.xpath(
      "/html/body/div[4]/div/div[2]/div/div[2]/div[3]/div[2]/div[2]/div[3]/div[3]/div[1]/div[2]/div/div[1]/div[1]/div/div[1]/div/h3/a/div[1]/text()"  
    ).get()

    url = response.xpath(
      "/html/body/div[4]/div/div[2]/div/div[2]/div[3]/div[2]/div[2]/div[3]/div[3]/div[1]/div[2]/div/div[1]/div[1]/div/div[1]/div/h3/a"
    ).attrib["href"]

    processed_data = {
      "hotel" : hotel,
      "url" : url,
    }
    yield processed_data





# If file exists, delete it 
if Path.exists(kCurrentDir/kOutFile):
  (kCurrentDir/kOutFile).unlink()
if Path.exists(kCurrentDir/kLogfile):
  (kCurrentDir/kLogfile).unlink()


# https://docs.scrapy.org/en/latest/topics/settings.html?highlight=settings#settings
process = CrawlerProcess(
  settings={
    # voir https://www.whatismybrowser.com/guides/the-latest-user-agent/chrome
    # je sais pas encore si tout est utilisable dans scrapy
    "USER_AGENT": "Chrome/97.0",
    "LOG_LEVEL": logging.INFO,  # CRITICAL, ERROR, WARNING, INFO, DEBUG...
    # https://docs.scrapy.org/en/latest/topics/logging.html#topics-logging
    "FEEDS": {
        str(kCurrentDir)
        + "/"
        + kOutFile: {
            "format": "json"
        },  # https://docs.scrapy.org/en/latest/topics/feed-exports.html#std-setting-FEEDS
    },
    # log dans fichier
    "LOG_STDOUT": False,
    "LOG_FILE": f"{kCurrentDir}/{kLogfile}",
  }
)


# A réactiver par la suite
# df = pd.read_csv(kCurrentDir/kCitiesFile)
# df.rename(columns={"Unnamed: 0": "id"}, inplace=True)

# list_villes = list(df["city"])
list_villes=["Aix en Provence"]
for ville in list_villes:
  my_start_urls = [
      f"https://www.booking.com/searchresults.fr.html?ss={ville}&checkin=2024-04-02&checkout=2024-04-05&group_adults=2&no_rooms=1&group_children=0",
  ]

  # HotelsListSpider.start_urls = my_start_urls
  process.crawl(HotelsListSpider, my_start_urls)
  process.start()


# nflt=ht_id
# https://www.booking.com/searchresults.fr.html?ss=Aix en Provence&checkin=2024-04-02&checkout=2024-04-05&group_adults=2&no_rooms=1&group_children=0&nflt=ht_id  











# data-atlas-latlng="49.27603159,-0.70172489"


# <a id="hotel_sidebar_static_map" class="loc_block_link_underline_fix 
# map_static_zoom show_map map_static_hover jq_tooltip map_static_button_hoverstate maps-more-static-focus txp-fix-hover 
# " href="#map_opened-hotel_sidebar_static_map" data-atlas-latlng="49.27603159,-0.70172489" data-lang-for-url="fr" data-action="hotel" data-api-key="AIzaSyDXrqUc7k84GZ0W6P5sMFrKFMVIdN-Nd0w" data-atlas-bbox="49.2580661691929,-0.729312459909215,49.2939970023391,-0.674137313879237" style=" height:200px; background: url(https://maps.googleapis.com/maps/api/staticmap?channel=hotel&amp;zoom=13&amp;size=264x200&amp;key=AIzaSyDXrqUc7k84GZ0W6P5sMFrKFMVIdN-Nd0w&amp;language=fr&amp;center=49.27603159,-0.70172489&amp;signature=7HMF15-FHLaSYqDjFzpZ74tuy_8=) center; " data-source="map_thumbnail" data-map-open-text="Retour à l'établissement" role="button">
# <div class="txp-map-cta-wrap">
# <button class="txp-map-cta bui-button bui-button--primary" data-map-open-text="Retour à l'établissement" data-map-thumb-label="">
# <span class="bui-button__text">
# Voir sur la carte
# </span>
# </button>
# </div>
# <span class="map-thumb__marker--current">
# <svg class="property-marker" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 18 29">
# <ellipse class="shadow" fill="#000000" fill-opacity="0.24" cx="9" cy="27" rx="6" ry="2"></ellipse>
# <path class="pin" d="M9,27 C7,27 0,16.9704016 0,9 C2.28269391e-16,4.02943725 4.02943725,0 9,0 C13.9705627,0 18,4.02943725 18,9 C18,16.9704016 11,27 9,27 Z M9,13 C11.209139,13 13,11.209139 13,9 C13,6.790861 11.209139,5 9,5 C6.790861,5 5,6.790861 5,9 C5,11.209139 6.790861,13 9,13 Z"></path>
# </svg>
# </span>
# </a>


            


            
            # }

# ma_liste = [
#   "Mont Saint Michel",
#   "St Malo",
#   "Bayeux",
#   "Le Havre",
#   "Rouen",
# ]



# https://www.booking.com/searchresults.fr.html?ss=Paris&checkin=2024-04-08&checkout=2024-04-12&group_adults=2&no_rooms=1&group_children=0
  



# Lire https://medium.com/@nikhilmalkari18/html-parsing-made-easy-extracting-data-with-scrap-in-python-671923d63ff8
# class HotelsSpider(scrapy.Spider):
#     name = "hotel"
#     ville = "Bayeux"
#     # template = f"https://www.booking.com/searchresults.fr.html?ss={ville}&checkin=2024-04-02&checkout=2024-04-05&group_adults=2&no_rooms=1&group_children=0"
    
#     start_urls = [
#         # "https://www.booking.com/",
#         # f"https://www.booking.com/searchresults.fr.html?ss={ville}&checkin=2024-04-02&checkout=2024-04-05&group_adults=2&no_rooms=1&group_children=0",
#         "https://www.booking.com/hotel/fr/reine-mathilde-bayeux.fr.html?aid=304142&label=gen173nr-1FCAQoggJCDXNlYXJjaF9iYXlldXhIDVgEaE2IAQGYAQ24ARfIAQzYAQHoAQH4AQOIAgGoAgO4AvOjsLAGwAIB0gIkNzFhZmZkMDItMDdjMS00NjFhLTgxNjItMDZmYzQzOWQ3M2U12AIF4AIB&sid=69e58baac330df6387e04bc169954cc2&all_sr_blocks=4352201_200988783_0_2_0;checkin=2024-04-02;checkout=2024-04-05;dist=0;group_adults=2;group_children=0;hapos=2;highlighted_blocks=4352201_200988783_0_2_0;hpos=2;matching_block_id=4352201_200988783_0_2_0;no_rooms=1;req_adults=2;req_children=0;room1=A%2CA;sb_price_type=total;sr_order=popularity;sr_pri_blocks=4352201_200988783_0_2_0__30180;srepoch=1712067955;srpvid=d09463b9bc9b02f4;type=total;ucfs=1&"
#     ]

    
#     def parse(self, response):
#         hotel = response.xpath(
#             "/html/body/div[4]/div/div[2]/div/div[2]/div[3]/div[2]/div[2]/div[3]/div[3]/div[1]/div[2]/div/div[1]/div[1]/div/div[1]/div/h3/a/div[1]/text()"  
#         ).get()

#         geo = response.xpath(
#             "/html/body/div[3]/div/div[4]/div[1]/div[1]/div[1]/div/div[2]/div[2]/a"
#         ).get()
#         numbers = re.findall('[+-]*\d+\.\d+', geo)
#         latitude = numbers[0]
#         longitude = numbers[1]

#         processed_data = {
#             # "hotel" : hotel,
#             "latitude" : latitude,
#             "longitude" : longitude,
#         }

#         yield processed_data
 
    
    
    # def parse(self, response):
        
    #     return {
    #         # Fonctionne
    #         "hotel": response.xpath(
    #             "/html/body/div[4]/div/div[2]/div/div[2]/div[3]/div[2]/div[2]/div[3]/div[3]/div[1]/div[2]/div/div[1]/div[1]/div/div[1]/div/h3/a/div[1]/text()"  
                
    #         ).get(),

    #         # Fonctionne PAS
    #         # "score": response.xpath(
    #         #     "/html/body/div[4]/div/div[2]/div/div[2]/div[3]/div[2]/div[2]/div[3]/div[5]/div[1]/div[2]/div/div[1]/div[2]/div/div/a/span/div/div[1]/text()"
    #         # ),


    #         # Fonctionne
    #         # "url": response.xpath(
    #         #     "/html/body/div[4]/div/div[2]/div/div[2]/div[3]/div[2]/div[2]/div[3]/div[3]/div[1]/div[2]/div/div[1]/div[1]/div/div[1]/div/h3/a"
    #         # ).attrib["href"],


    #         # A faire tourner sur une page d'hotel
    #         # "geo":response.xpath(
    #         #     "/html/body/div[3]/div/div[4]/div[1]/div[1]/div[1]/div/div[2]/div[2]/a/@href"
    #         # ).extract_first(),
    #         # "geo":response.xpath(
    #         #     "/html/body/div[3]/div/div[4]/div[1]/div[1]/div[1]/div/div[2]/div[2]/a"
    #         # ).get(),

    #         geo = response.xpath(
    #             "/html/body/div[3]/div/div[4]/div[1]/div[1]/div[1]/div/div[2]/div[2]/a"
    #         ).get()
    #         numbers = re.findall('[+-]*\d+\.\d+', str)
    #         # latitude = re.findall("\d+\.\d+", "Current Level: 13.4db.")
    #         latitude = numbers[0]
    #         longitude = numbers[1])

    #         "latitude" : latitude,
    #         "longitude" : longitude,         
            
            
    #         # get() recupère toute la chaine       
    #         #.attrib["href"], # recupère que l'url href="#map_opened-hotel_sidebar_static_map"
            

"""
