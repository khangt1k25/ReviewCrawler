import scrapy
from ..items import AirbnbItem
from scrapy.spiders import CrawlSpider

listing_url_base = 'https://www.airbnb.com.vn/api/v3/ExploreSearch?operationName=ExploreSearch&locale=vi&currency=USD&_cb=133mcs6c59fhj&variables={"request":{"metadataOnly":false,"version":"1.7.9","itemsPerGrid":20,"refinementPaths":["/homes"],"flexibleTripDates":["april","may"],"flexibleTripLengths":["weekend_trip"],"datePickerType":"calendar","searchType":"pagination","tabId":"home_tab","placeId":"ChIJOwg_06VPwokRYv534QaPC8g","federatedSearchSessionId":"85465201-250d-4b57-ba9f-a552dff4781d","itemsOffset":%s,"sectionOffset":3,"query":"New York, NY, United States","cdnCacheSafe":false,"simpleSearchTreatment":"simple_search_only","treatmentFlags":["storefronts_feb_2021_homepage_web","simple_search_1_1","simple_search_desktop_v3_full_bleed","flexible_dates_options_extend_one_three_seven_days","super_date_flexibility","search_input_placeholder_phrases"],"screenSize":"large"}}&extensions={"persistedQuery":{"version":1,"sha256Hash":"9d182f66a3e7364981c484a0f0f138fb95506054f95361e3a01e065b60d7a6f4"}}'
review_url_base = 'https://www.airbnb.com.vn/api/v3/PdpReviews?operationName=PdpReviews&locale=vi&currency=USD&_cb=za47gp1509tww&variables={"request":{"fieldSelector":"for_p3","limit":7,"listingId":"%s","numberOfAdults":"1","numberOfChildren":"0","numberOfInfants":"0","offset":"%d"}}&extensions={"persistedQuery":{"version":1,"sha256Hash":"d849102acaf2479c6c0fc02cdbbc68dfb540772b48ebcd9e99962314d5743f23"}}'
headers = {
    'authority': "www.airbnb.com.vn",
    'method': 'GET',
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept_language': 'en-US,en;q=0.9,vi;q=0.8',
    'content-type': 'application/json',
    'Sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
    'Sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
    'X-airbnb-api-key': 'd306zoyjsyarp7ifhu67rjxn52tv0t20',
    'X-airbnb-graphql-platform': 'web',
    'X-airbnb-graphql-platform-client': 'apollo-nlobe',
    'X-CSRF-Token': 'V4$.airbnb.com.vn$Gxu341x2JzU$IdbnEcUVaRGDHeSGAe4EvNxRsSgnndWi6TAcfSiK0H4=',
    'X-CSRF-Without-Token': 1
}


class ReviewSpider(CrawlSpider):

    name = 'review'
    start_urls = [listing_url_base % i for i in range(1, 301, 20)]

    # Start to get API list of listing_ids
    def start_requests(self):

        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                headers=headers,
                callback=self.parse
            )

    # Parse to get API review of listing
    def parse(self, response):

        jsonfile = response.json()
        jsonitems = jsonfile['data']['dora']['exploreV3']['sections'][0]['items']

        for item in jsonitems:
            listing_id = item['listing']['id']
            for review_id in range(0, 100, 7):
                yield scrapy.Request(
                    url=review_url_base % (listing_id, int(review_id)),
                    headers=headers,
                    callback=self.parse_review
                )

    # Parse to extract review
    def parse_review(self, response):

        jsonfile = response.json()
        reviews = jsonfile['data']['merlin']['pdpReviews']['reviews']

        for review in reviews:
            yield AirbnbItem(
                text=review['comments'],
                rating=review['rating']
            )
