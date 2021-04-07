from scrapy.loader.processors import TakeFirst, MapCompose, Join, Compose
from scrapy.loader import ItemLoader



class AirbnbLoader(ItemLoader):
    default_output_processor = TakeFirst()
    