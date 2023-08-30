import scrapy
import uuid
import re
import http.client
from locations.categories import Code
from locations.items import GeojsonPointItem

class Taza_Sa_Spider(scrapy.Spider):
    name = "taza_sa_dac"
    brand_name = "Al Tazaj"
    spider_type = "chain"
    spider_categories = [Code.RESTAURANT]
    #spider_countries = [pycountry.countries.lookup('sa').alpha_3]
    allowed_domains=["taza.com.sa"]
    start_urls = ["https://www.taza.com.sa/pages/branches"]
    
    def parse(self, response):
        address_list = response.xpath('//div[contains(@class, "sc-egiyK kKHsVi pf")]//p[contains(@class, "sc-gDGHff eHTxVX pf")]//span//text()').getall()
        location_links = response.xpath('//div[contains(@class, "sc-egiyK kKHsVi pf")]//div[contains(@class, "sc-ywFzA hSgvfU pf")]//a/@href').getall()
        latitude = []
        longitude = []
        for link in location_links:
            match = re.search(r'@(-?\d+\.\d+),(-?\d+\.\d+)', link)
            if match:
                latitude.append(float(match.group(1)))
                longitude.append(float(match.group(2)))
                print(float(match.group(1)), float(match.group(2)))
            else:
                conn = http.client.HTTPSConnection("goo.gl")
                conn.request("HEAD", link)
                response = conn.getresponse()
                expanded_url = response.headers.get('location')
                conn.close()

                if expanded_url:
                    match = re.search(r'@(-?\d+\.\d+),(-?\d+\.\d+)', expanded_url)
                    if match:
                        latitude.append(float(match.group(1)))
                        longitude.append(float(match.group(2)))
                        #print(float(match.group(1)), float(match.group(2)))
                    else:
                        latitude.append('')
                        longitude.append('')
                else:
                    latitude.append('')
                    longitude.append('')
                
        for i, address in enumerate(address_list):
            data = {
                "ref": str(uuid.uuid4()),
                "chain_name": "Al Tazaj",
                "chain_id": "1885",
                "lat" : latitude[i],
                "lon" : longitude[i],
                "name": "Al Tazaj",
                "addr_full": address.strip(),
                "country": "Saudi Arabia",
                "website": "https://www.taza.com.sa",
            }
            yield GeojsonPointItem(**data)