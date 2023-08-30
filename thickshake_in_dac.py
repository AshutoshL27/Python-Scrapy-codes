import scrapy
import uuid
import re
from locations.categories import Code
from locations.items import GeojsonPointItem

class Thickshake_Factory_Spider(scrapy.Spider):
    name = "thickshakefactory_ind_dac"
    brand_name = "The Thickshake Factory"
    spider_type = "chain"
    spider_categories = [Code.RESTAURANT]
    #spider_countries = [pycountry.countries.lookup('sa').alpha_3]
    allowed_domains=["thethickshakefactory.com"]
    start_urls = ["https://store.thethickshakefactory.com"]
    
    def parse(self, response):
        shop_details=[]
        shop_details_list = response.css('.store-info-box')

        for shop in shop_details_list:
            lat = shop.css('.outlet-latitude::attr(value)').get()
            long = shop.css('.outlet-longitude::attr(value)').get()
            
            phone_link = shop.css('.outlet-phone a::attr(href)').get()
            phone = phone_link.replace('tel:+', '')
            
            address_lines = shop.css('.outlet-address span::text').getall()
            address = ' '.join(line.strip() for line in address_lines)
            
            postcode = re.search(r'\b\d{6}\b', address)
            postcode = postcode.group() if postcode else None
            
            city = re.search(r'(\w+)\s*-', address)
            city = city.group(1) if city else None 
            
            website_url=shop.css('a.btn-website::attr(href)').get() 
            
            shop_info = {
                'address': address,
                'city': city,
                'phone': phone,
                'postcode': postcode,
                'latitude': lat,
                'longitude': long,
                'website': website_url
            }
            shop_details.append(shop_info)
        
        next_page_link = response.css('.pagination li.next a::attr(href)').get()
        if next_page_link:
            yield response.follow(next_page_link, callback=self.parse)
            
        for i in shop_details:
            data = {
                "ref": str(uuid.uuid4()),
                "chain_name": "The Thickshake Factory",
                "chain_id": "34196",
                "lat" : i['latitude'],
                "lon" : i['longitude'],
                "name": "The Thickshake Factory",
                "addr_full": i['address'],
                "city" : i['city'],
                "postcode":i['postcode'],
                "country": "India",
                "phone" : i['phone'],
                "website": i['website'],
            }
            yield GeojsonPointItem(**data)