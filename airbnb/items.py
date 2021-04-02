import scrapy

# Review Airbnb Item


class AirbnbItem(scrapy.Item):
    text = scrapy.Field()
    rating = scrapy.Field()
