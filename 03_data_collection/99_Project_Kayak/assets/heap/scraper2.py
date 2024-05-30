from pathlib import Path
import logging
import scrapy
from scrapy.crawler import CrawlerProcess
import pandas as pd

kCitiesFile = "cities.csv"
kLogfile    = "scrapy.log"
kOutFile    = "kayak.json"
kCurrentDir = Path(__file__).parent

# -----------------------------------------------------------------------------
class HotelsListSpider(scrapy.Spider):

  name = "HotelsListSpider"

  def start_requests(self):
    
    # A réactiver par la suite
    # df = pd.read_csv(kCurrentDir/kCitiesFile)
    # df.rename(columns={"Unnamed: 0": "id"}, inplace=True)
    # list_villes = list(df["city"])
    list_villes=["Aix en Provence", "Marseille"]
    urls=[]
    for ville in list_villes:
      urls.append(
        f"https://www.booking.com/searchresults.fr.html?ss={ville}&checkin=2024-05-02&checkout=2024-05-05&group_adults=2&no_rooms=1&group_children=0",
      )
    
    for url in urls:
      yield scrapy.Request(url=url, callback=self.parse)


  


  # lire https://docs.scrapy.org/en/latest/intro/tutorial.html
  def parse(self, response):
    ma_list = response.css("div[data-testid='title']::text") #property-card
    for h in ma_list:
      print(h.get())
    
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



# -----------------------------------------------------------------------------
if __name__ == "__main__":

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