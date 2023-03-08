import scrapy, json, re
from scrapy.shell import inspect_response
from scrapy.crawler import CrawlerProcess

class BeachesScraper(scrapy.Spider):
    name = 'BeachesScraper'

    with open("config.json") as file:
        scraper_config = json.load(file)
    
    # declare start urls
    start_urls = scraper_config.get("start_urls")

    custom_settings = {
        'DOWNLOAD_DELAY' : 0.5,
        'RETRY_TIMES': 10,

        # export as json format
        'FEED_FORMAT' : 'json',
        'FEED_URI' : scraper_config.get("output_file")
    }

    def parse(self, response):
        view_all_link = response.css(self.scraper_config.get("selectors").get("view_all_beaches_css")).extract_first()
        object_id = re.search('object_id=(\d+)', view_all_link).group(1)
        url = "https://beachsearcher.com/en/searchMain?object=country&object_id={}&smart=0&pagesize=18&offset=0"
        yield scrapy.Request(url=url.format(object_id), callback=self.beaches_api_parse)

    def beaches_api_parse(self, response):
        data = response.json()
        all_count = data.get("AllCount")
        beaches = data.get("Beaches")
        offset = data.get("Offset")
        new_offset = offset + 18
        if new_offset < all_count:
            yield scrapy.Request(response.url.rstrip(str(offset)) + str(new_offset), callback=self.beaches_api_parse)

        for beach in beaches:
            _id = beach.get("id")
            slug = beach.get("slug")
            beach_url = f"https://beachsearcher.com/en/beach/{_id}/{slug}"
            features = json.loads(beach.get("features"))

            try:
                beach_tags = [features.get("audience").get("label")]
            except:
                beach_tags = []

            map_url= beach_url + "/map"
            coordinates = re.search("\((.*)\)", beach.get("point")).group(1).split()
            yield scrapy.Request(beach_url, callback=self.beach_parsed, meta={
                "beach_tags": [beach_tags],
                "map_url": map_url,
                "coordinates": coordinates
            })

    def beach_parsed(self, response):

        try:
            width = response.xpath("//a[contains(text(), 'Width - ')]/text()").extract_first().replace("Width - ", "")
        except:
            width = ""

        try:
            shore_shape = response.xpath("//a[contains(text(), 'Shore shape - ')]/text()").extract_first().replace("Shore shape - ", "")
        except:
            shore_shape = ""

        try:
            length = response.xpath("//a[contains(text(), 'Length - ')]/text()").extract_first().replace("Length - ", "")
        except:
            length = ""

        yield {
            "beach_url": response.url,
            "beach_supertitle": response.css("div.beach-desc__booking-city::text").extract_first(),
            "beach_title": response.css("div.beach-desc__title > h1::text").extract_first().strip(),
            "beach_subtitle": response.css("div.beach-desc__title > h3::text").extract_first().strip(),
            "beach_tags": response.meta.get("beach_tags"),
            "beach_rating": response.css("div.beach-desc__points::text").extract_first(),
            "beach_rank": response.css("div.beach-desc__out::text").extract_first().strip(),
            "map_url": response.meta.get("map_url"),
            "coordinates": response.meta.get("coordinates"),
            "key_features": response.css("li.beach-top-special__item span::text").extract(),
            "water_score": response.xpath("//div[text()='Water']/../following-sibling::div[1]/div[2]/text()").extract_first().strip().split('/')[0],
            "cover_score": response.xpath("//div[text()='Cover']/../following-sibling::div[1]/div[2]/text()").extract_first().strip().split('/')[0],
            "cleanliness": response.xpath("//div[text()='Cleanliness']/../following-sibling::div[1]/div[2]/text()").extract_first().strip().split('/')[0],
            "amenities": response.xpath("//div[text()='Amenities']/../following-sibling::div[1]/div[2]/text()").extract_first().strip().split('/')[0],
            "natural features": response.xpath("//h3[text()='Natural features']/following-sibling::ul/div/li/a/text()").extract(),
            "general_features": response.xpath("//div[text()='ownership']/../following-sibling::div[1]/li/a/text()").extract(),
            "occupancy": response.xpath("//div[text()='occupancy']/../following-sibling::div[1]/li/a/text()").extract_first(),
            "sharks": response.xpath("//div[text()='sharks']/../following-sibling::div[1]/li/a/text()").extract_first(),
            "size_and_shape": {
                "width": width,
                "shore_shape": shore_shape,
                "length": length
            },
            "location_text": response.xpath("//div[text()='location']/../following-sibling::div[1]/li/a/text()").extract_first(),
            "access": response.xpath("//h3[text()='Access']/following-sibling::ul/div/li/a/text()").extract(),
            "cover_and_water": response.xpath("//div[text()='cover']/../following-sibling::div[1]/li/a/text()").extract(),
            "swimming_details": response.xpath("//div[text()='swimming details']/../following-sibling::div[1]/li/a/text()").extract(),
            "water": response.xpath("//div[text()='water']/../following-sibling::div[1]/li/a/text()").extract(),
            "rental": response.xpath("//h3[text()='Rental']/following-sibling::ul/div/li/a/text()").extract(),
            "audience": response.xpath("//h3[text()='Audience']/following-sibling::ul/div/li/a/text()").extract(),
            "infrastructure": response.xpath("//h3[text()='Infrastructure']/following-sibling::ul/div/li/a/text()").extract()
        }

process = CrawlerProcess()
process.crawl(BeachesScraper)
process.start()