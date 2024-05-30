import pandas as pd
from pathlib import Path
import scrapy
from scrapy.crawler import CrawlerProcess
import logging


class FilmSpider(scrapy.Spider):
    name = "randomquote"
    start_urls = [
        "https://www.imdb.com/title/tt21235248/?ref_=chtbo_t_1",
    ]

    def parse(self, response):
        return {
          # CAST OK
          # Correction  /html/body/div[2]/main/div/section[1]/div/section/div/div[1]/section[@data-testid="title-cast"]/div[2]/div[2]/div                 div[2]/a/text()
          # actor 1     /html/body/div[2]/main/div/section[1]/div/section/div/div[1]/section[3]                        /div[2]/div[2]/div[1]/div[2]/a
          # actor 2     /html/body/div[2]/main/div/section[1]/div/section/div/div[1]/section[3]                        /div[2]/div[2]/div[2]/div[2]/a
          # Fonctionne
          #"cast": [actor.xpath('div[2]/a/text()').get() for actor in response.xpath('/html/body/div[2]/main/div/section[1]/div/section/div/div[1]/section[@data-testid="title-cast"]/div[2]/div[2]/div')],
          # "cast": [actor.xpath('div[2]/a/text()').get() for actor in response.xpath('/html/body/div[2]/main/div/section[1]/div/section/div/div[1]/section[3]/div[2]/div[2]/div')],


          # STORYLINE NOK
          # FullXPath                    /html/body/div[2]/main/div/section[1]/div/section/div/div[1]/section[6]/div[2]/div[1]/div/div/div
          # Correction                   /html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/section/p/span[2]/text()  
          # Fonctionne  
          # "storyline": response.xpath('/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/section/p/span[2]/text()').get(),


          # GENRE OK
          # Fonctionne
          #"genres": [genre.xpath('span/text()').get() for genre in response.xpath('/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/section/div[1]/div[2]/a')], 
          # FullXPath /html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/section/div[1]/div[2]/a[2]/span
          #           /html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/section/div[1]/div[2]/a[1]/span  
          # "genres": [genre.xpath('span/text()').get() for genre in response.xpath('/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/section/div[1]/div[2]/a')], 


          # TITLE OK
          # Fonctionne  
          #                        /html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/h1/span
          # "title": response.xpath('/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/h1/span/text()').get(),


          # URL
          # def process_request(self, request, spider): 
          #   # avoid infinite loop by not processing the URL if it contains the desired part
          #   if "hello%20world" in request.url: 
          #       pass 

          #   new_url = request.url + "hello%20world"
          #   request = request.replace(url=new_url) 
          #   return request 
          "url": response.url.replace("https://www.imdb.com", ''),  


            
                                                                                   
            # "page": response.xpath(
            #     "/html"  
            # ).get(),
            
            # "fifi": response.xpath(
            #     "/html/body/div/div[2]/div[1]/div/span[2]/small/text()"
            # ).get(),
            # "loulou": response.xpath(
            #     "/html/body/div/div[2]/div[1]/div/div/a/text()"
            # ).getall(),
            # difference entre get() et getall()
            # .get() always returns a single result
            #     if there are several matches, content of a first match is returned;
            #     if there are no matches, None is returned.
            # .getall() returns a list with all results.
            # get()
            # [
            #   {"storyline": null}
            # ]
            # 

            # getall()
            # [
            #   {"storyline": []}
            # ]
            
        }
    



# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
if __name__ == '__main__':

  # filename = "url_list.txt"
  # current_dir = Path(__file__).parent

  # df = pd.read_csv(current_dir / filename)
  # print(df) 

  # for url in df["url"]:
  #   print(url)


  # url = "https://www.imdb.com/title/tt21235248/?ref_=chtbo_t_1"

  filename = "imdb3.json"
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
      "USER_AGENT": "Chrome/123.0",
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

  process.crawl(FilmSpider)
  process.start()

