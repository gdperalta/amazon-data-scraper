import scrapy
import re
import json
from urllib.parse import urlencode


queries = ['tshirt for men']
class AmazonSpider(scrapy.Spider):
    name = "amazon"
    def start_requests(self):
        for query in queries:
            url = 'https://www.amazon.com/s?' + urlencode({'k': query})
            yield scrapy.Request(url=self.get_url(url), callback=self.parse_keyword_response)


    def parse_keyword_response(self, response):
        products = response.xpath('//*[@data-asin]')
        for product in products:
            asin = product.xpath('@data-asin').extract_first()
            product_url = f"https://www.amazon.com/dp/{asin}"
            yield scrapy.Request(url=self.get_url(product_url), callback=self.parse_product_page, meta={'asin': asin})
        # To scrape all pages
        # next_page = response.xpath('//li[@class="a-last"]/a/@href').extract_first()
        # if next_page:
        #     url = urljoin("https://www.amazon.com",next_page)
        #     yield scrapy.Request(url=self.get_url(url), callback=self.parse_keyword_response)


    def parse_product_page(self, response):
        seller_url = response.xpath('//*[@id="bylineInfo"]/@href').extract_first()
        seller_name = response.xpath('//*[@id="bylineInfo"]/text()').extract_first()
        asin = response.meta['asin']
        title = response.xpath('//*[@id="productTitle"]/text()').extract_first()
        # image = re.search('"large":"(.*?)"',response.text).groups()[0]
        rating = response.xpath('//*[@id="acrPopover"]/@title').extract_first()
        number_of_reviews = response.xpath('//*[@id="acrCustomerReviewText"]/text()').extract_first()
        # price = response.xpath('//*[@id="priceblock_ourprice"]/text()').extract_first()
        # if not price:
        #     price = response.xpath('//*[@data-asin-price]/@data-asin-price').extract_first() or \
        #             response.xpath('//*[@id="price_inside_buybox"]/text()').extract_first()
        # temp = response.xpath('//*[@id="twister"]')
        # sizes = []
        # colors = []
        # if temp:
        #     s = re.search('"variationValues" : ({.*})', response.text).groups()[0]
        #     json_acceptable = s.replace("'", "\"")
        #     di = json.loads(json_acceptable)
        #     sizes = di.get('size_name', [])
        #     colors = di.get('color_name', [])
        # bullet_points = response.xpath('//*[@id="feature-bullets"]//li/span/text()').extract()
        seller_rank = response.xpath('//*[text()="Best Sellers Rank:"]/parent::*//text()[not(parent::style)]').extract()
        yield {'SellerUrl': seller_url, 'SellerName': seller_name, 'asin': asin, 'Title': title, 'Rating': rating, 'NumberOfReviews': number_of_reviews, 'SellerRank': seller_rank}

    
    def get_url(self, url):
        API_KEY = '603538f20599863705cc3bf82a543435'
        payload = {'api_key': API_KEY, 'url': url, 'country_code': 'au'}
        proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload)
        return proxy_url