# Readme

## Files of the project
1. ``kayak_part1.ipynb``
1. ``kayak_part2.ipynb``
    1. `scraper7_attributes.py`
    1. `scraper8_hotels_per_city.py`


## How to use the project
1. Open and run ``kayak_part1.ipynb``
    * It generates one file `.\Project_Kayak\assets\cities.csv`
    * It also display the ranked cities on a map 
1. Open and run ``kayak_part2.ipynb``
    * Based on the content of `\assets\cities.csv` it generate diffrents intermediates files
    * All the intermediates and log files are stored in ``./assets`` directory
    * In addition to cities.csv you should find 
        * ``hotels_attributes.json`` : list of attributes (comment, lon, lat...) for each hotel of the current town
        * ``hotels_list.json`` : list of hotels for the current town
        * ``scrapy.log`` : the log of the last scraping session
        * ``travel_data.csv`` : the file with all the collected data. It is a copy of the csv file available on S3 
        * ``travel_data.sql`` : sql schema of travel_date.csv
        * ``travel_data.sqlite`` : sqlite version of the travel_date.csv 
        * Few .png files





## Testing scrapy 
* In order to "play" with scrapy
* In VSCODE
* Open a terminal
* Type `scrapy shell "https://quotes.toscrape.com/page/1/"`
* Read https://docs.scrapy.org/en/latest/intro/tutorial.html
* Type ``exit`` to quit

