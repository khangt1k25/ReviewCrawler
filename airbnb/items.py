import scrapy

class AirbnbItem(scrapy.Item):
    review_id = scrapy.Field()
    reviewer_id = scrapy.Field()
    reviewee_id = scrapy.Field()
    text = scrapy.Field()
    rating = scrapy.Field()
    date = scrapy.Field()
