from pathlib import Path
import logging
import scrapy
from scrapy.crawler import CrawlerProcess

kCitiesFile = "cities.csv"
kLogfile    = "scrapy.log"
kOutFile    = "hotel_attributes.json"
kCurrentDir = Path(__file__).parent

class OneHotelSpider(scrapy.Spider):
    name = "OneHotelSpider"
    start_urls = [
      #"https://www.booking.com/hotel/fr/ha-tel-marseille-vieux-port.fr.html",
      #"https://www.booking.com/hotel/fr/hotelkyriadrabatau.fr.html",
      "https://www.booking.com/hotel/fr/citea-marseille-prado-perier.fr.html",
    ]

    


    def parse(self, response):
      kScoreSelector        = '.a3b8729ab1.d86cee9b25::text'
      kDescription1Selector = 'property_description_content::text'  # <div id="property_description_content" ...
      kDescription2Selector = '.a53cbfa6de.b3efd73f69::text'        # <p data-testid="property-description" class="a53cbfa6de b3efd73f69">....
      # klatlng = ".hotel-sidebar-map hotel-sidebar-map-a11y::attr(href)"         # <div class="hotel-sidebar-map hotel-sidebar-map-a11y">....
      klatlng = "div.hotel-sidebar-map hotel-sidebar-map-a11y a::attr(href)"         # <div class="hotel-sidebar-map hotel-sidebar-map-a11y">....

      score = response.css(kScoreSelector).get().replace(",", ".")  
      # print(score)
      
      # url = response.css(klatlng).extract()
      url = response.css("div.hotel-sidebar-map a::attr(data-atlas-latlng)").extract()
      latitude = url[0].split(",")[0]
      longitude = url[0].split(",")[1]
      # print(latitude, longitude)

      description = response.css(kDescription2Selector).get()
      # print(description)

      processed_data = {
           "score"        : score,
           "latitude"     : latitude,
           "longitude"    : longitude,
           "description"  : description,
         }
      yield processed_data






      # for hotel in :
      #   hotel_name = hotel.css(kNameSelector).extract_first()
      #   url = hotel.css(kUrlSelector).get().split("?")[0]

      #   processed_data = {
      #     "hotel" : hotel_name,
      #     "url"   : url,
      #   }
      #   yield processed_data



      
      

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

process.crawl(OneHotelSpider)
process.start()


# <div id="property_description_content" data-et-view="THHSODPNGZfSeUHMDXCFKOLYHe:1 ">
# Vous pouvez bénéficier d'une réduction Genius dans l'établissement Hôtel Marsiho by HappyCulture - ex Best Western Marseille&nbsp;! <a href="https://account.booking.com/auth/oauth2?redirect_uri=https%3A%2F%2Fsecure.booking.com%2Flogin.html%3Fop%3Doauth_return&amp;aid=304142&amp;bkng_action=hotel&amp;dt=1712395784&amp;state=UoECdXuPjOlHa0jcPz_7_VlWkiWtgPCSvRVLyOjWLEmNbpefdJ6E95L450Xt30G_-UIXOQui5cmbMn0nhIMA6Z3Xu67vbHF2c8XnfQkAz5GYaElNRqQXse_5l886sUZnVMwNyI2RlyymPe-XdIIHoigvqfjK8MKMu--CyTG3no2vige56VcjhFWT70ODTCigPvuAEx0GUMKZY0DV2E7i_dh8gu0Df3-SO9GjLXkmXvS5XdmeZU6K2aVDJmeTp77llXBwrk4GUIfEJO_H5-if1cXlcz6EEcy3mvyWbF-KLWEzQsJEcJDDXSQBVuUOoXMBXy1aesQjfXTWi480RLCti8qoQrw&amp;client_id=vO1Kblk7xX9tUn2cpZLS&amp;lang=fr&amp;response_type=sso" class="bui-link">Connectez-vous</a> pour économiser.
# <div data-capla-component-boundary="b-property-web-property-page/PropertyDescriptionDesktop" data-capla-hydration="0"><p data-testid="property-description" class="a53cbfa6de b3efd73f69">Situé dans le centre de Marseille, le Hôtel Marsiho by HappyCulture - ex Best Western Marseille propose 51&nbsp;chambres à la décoration moderne avec connexion Wi-Fi gratuite. La réception est ouverte 24h/24. Le Vieux-Port de Marseille est accessible en seulement 5&nbsp;minutes à pied.

# Toutes les chambres insonorisées sont dotées de la climatisation et d'une télévision à écran plat. Chaque logement comprend une salle de bains privative pourvue d’une baignoire ou d’une douche.

# Tous les matins, l’établissement sert un petit-déjeuner buffet sur place.

# Vous pourrez profiter d’une station de recharge pour téléphones portables et d’une machine à café Nespresso dans les parties communes.

# L’hôtel se trouve à 350&nbsp;mètres de l’avenue de La Canebière et à 800&nbsp;mètres de&nbsp;la gare Saint-Charles.</p></div> 
# </div>






# <div class="hotel-sidebar-map hotel-sidebar-map-a11y">
# <a id="hotel_sidebar_static_map" class="loc_block_link_underline_fix 
# map_static_zoom show_map map_static_hover jq_tooltip map_static_button_hoverstate maps-more-static-focus txp-fix-hover 
# " href="#map_opened-hotel_sidebar_static_map" data-atlas-latlng="43.30046625,5.37444157" data-lang-for-url="fr" data-action="hotel" data-api-key="AIzaSyDXrqUc7k84GZ0W6P5sMFrKFMVIdN-Nd0w" data-atlas-bbox="43.2825008348766,5.34971036681283,43.3184316680228,5.39917277921993" style="height: 200px; background: url(&quot;https://maps.googleapis.com/maps/api/staticmap?key=AIzaSyDXrqUc7k84GZ0W6P5sMFrKFMVIdN-Nd0w&amp;zoom=13&amp;size=264x203&amp;language=fr&amp;channel=hotel&amp;center=43.30046625,5.37444157&amp;signature=_JdtJwM66_-MxOxstHFaLipSG9s=&quot;) center center;" data-source="map_thumbnail" data-map-open-text="Retour à l'établissement" role="button">
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
# </div>



# <p data-testid="property-description" class="a53cbfa6de b3efd73f69">Doté d'une connexion Wi-Fi gratuite, le Staycity Aparthotels Marseille Centre Vieux Port propose un hébergement climatisé à Marseille, à seulement 550&nbsp;mètres du port. L’établissement est situé à 12&nbsp;minutes de marche de la gare de Marseille-Saint-Charles.

# Tous les appartements et studios sont accessibles par un ascenseur et disposent d'une télévision à écran plat. Leur kitchenette est équipée d'un lave-vaisselle, d'un micro-ondes, d'un grille-pain, d'un réfrigérateur, de plaques de cuisson, d'une machine à café et d'une bouilloire. Les logements sont tous munis d’une salle de bains privative avec des articles de toilette gratuits. Les serviettes et le linge de lit sont fournis.

# Vous trouverez des bars, des boutiques et des restaurants à moins de 2&nbsp;minutes de marche.

# La station de métro la plus proche se trouve à seulement 44&nbsp;mètres. La Canebière est à 1&nbsp;km et le stade Vélodrome vous attend à 6,4&nbsp;km. L’aéroport Marseille-Provence, le plus proche de l’établissement, se trouve à 24&nbsp;km.

# Certains logements possèdent un balcon.</p>



# <div class="hotel-sidebar-map hotel-sidebar-map-a11y">
# <a id="hotel_sidebar_static_map" class="loc_block_link_underline_fix map_static_zoom show_map map_static_hover jq_tooltip map_static_button_hoverstate maps-more-static-focus txp-fix-hover 
# " href="#map_opened-hotel_sidebar_static_map" data-atlas-latlng="43.29732159,5.37753899" data-lang-for-url="fr" data-action="hotel" data-api-key="AIzaSyDXrqUc7k84GZ0W6P5sMFrKFMVIdN-Nd0w" data-atlas-bbox="43.2793561698367,5.35280906119177,43.3152870029829,5.4022689155294" style="height: 200px; background: url(&quot;https://maps.googleapis.com/maps/api/staticmap?channel=hotel&amp;size=264x215&amp;zoom=13&amp;key=AIzaSyDXrqUc7k84GZ0W6P5sMFrKFMVIdN-Nd0w&amp;center=43.29732159,5.37753899&amp;language=fr&amp;signature=lMg3qLzkSfMS2-Xvlh7eJK7_KBM=&quot;) center center;" data-source="map_thumbnail" data-map-open-text="Retour à l'établissement" role="button">
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
# </div>

