import scrapy
import uuid
import re
from locations.categories import Code
from locations.items import GeojsonPointItem

class AABSweets_Ind_Spider(scrapy.Spider):
    name = "aabseets_ind_dac"
    brand_name = "Adyar Ananda Bhavan"
    spider_type = "chain"
    spider_categories = [Code.RESTAURANT]
    allowed_domains = ["aabsweets.com"]
    start_urls = [
        "https://aabsweets.com/assets/json/location.json",                      #for stores in India
        "https://aabsweets.com/assets/json/international_location.json?v=1"     #for stores outside India
    ]

    def parse(self, response):
        if "json/location.json" in response.url:
            yield from self.parse_location(response)                    #for stores in India
        elif "international_location.json" in response.url:
            yield from self.parse_international_location(response)      #for stores outside India

    def parse_location(self, response):                                 #for stores in India
        data = response.json()
        for item in data:
            data = {
                "ref": str(uuid.uuid4()),
                "chain_name": "Adyar Ananda Bhavan",
                "chain_id": "32679",
                "name": item['Branches'],
                "addr_full": item['Address'],
                "country": "India",
                "phone": re.sub(r"\D", "", item['Phone']),
                "website": "https://aabsweets.com",
                #"lat":item['Latitude'],                     #This line extracts latitude information, site itself contains wrong info
                #"lon":item['Longitude']                     #This line extracts latitude information, site itself contains wrong info
            }
            yield GeojsonPointItem(**data)

    def parse_international_location(self, response):                   #for stores outside India
        data = response.json()
        for item in data:
            data = {
                "ref": str(uuid.uuid4()),
                "chain_name": "Adyar Ananda Bhavan",
                "chain_id": "32679",
                "name": item['Branches'],
                "addr_full": item['Address'],
                "country": item['Category'],  
                "phone": re.sub(r"\D", "", item['Phone']),
                "website": "https://aabsweets.com",
                #"lat":item['Latitude'],               #This line extracts latitude information, site itself contains wrong info
                #"lon":item['Longitude']               #This line extracts latitude information, site itself contains wrong info
            }
            yield GeojsonPointItem(**data)
