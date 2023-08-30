import scrapy
import re
import uuid
from locations.categories import Code
from locations.items import GeojsonPointItem

class Akron_Mx_Spider(scrapy.Spider):
    name = "akron_mx_dac"
    brand_name = "Akron"
    spider_type = "generic"
    spider_categories = [Code.PETROL_GASOLINE_STATION]
    #spider_countries = [pycountry.countries.lookup('mx').alpha_3]
    allowed_domains=["akron.com.mx"]
    start_urls = ["https://akron.com.mx/"]

    def parse(self, response):
        
        '''
        @url https://akron.com.mx/
        @returns items 1 2
        @scrapes ref addr_full housenumber street city state postcode country phone website lat lon
        '''
        
        response_list = response.xpath('//div[@class="textwidget custom-html-widget"]/div/a/text()').getall()
        location_link = response.xpath('//div[@id="custom_html-6"]/div[@class="textwidget custom-html-widget"]/div/a/@href').get()
        address_parts = re.split(r"[,]+", response_list[2])
        
        data = {
                "ref" : str(uuid.uuid4()),
                "chain_name" : "Akron",
                "chain_id" : "33995",
                "lat" : location_link.split('@')[1].split(',')[0],
                "lon" : location_link.split('@')[1].split(',')[1].split(',')[0],
                "name" : "Akron",
                "addr_full" : response_list[2],
                "housenumber" : address_parts[0].strip(), 
                "street" : address_parts[1].strip(),  
                "city" : address_parts[2].strip(),
                "state" : address_parts[3].strip(),
                "postcode" : address_parts[5].strip(),
                "country" : address_parts[4].strip(),
                "phone" : response_list[1].replace(" ", ""),
                "email" : response_list[0], 
                "website" : self.start_urls[0],  
            }
        yield GeojsonPointItem(**data)
