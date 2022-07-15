import scrapy
from urllib.parse import urlencode


queries = ['tshirt for men']
base_url = 'https://www.amazon.com.au'
class AmazonSpider(scrapy.Spider):
    name = "amazon"
    def start_requests(self):
        for query in queries:
            # url = f'{base_url}/s?' + urlencode({'k': query})
            url = 'https://www.amazon.com.au/gp/bestsellers/kitchen'
            yield scrapy.Request(url=self.get_url(url), callback=self.parse_keyword_response)


    def parse_keyword_response(self, response):
        # products = response.xpath('//*[@data-asin]')
        products = response.xpath('//*[@class="zg-grid-general-faceout"]/div/@id')
        for product in products:
            # asin = product.xpath('@data-asin').extract_first()
            asin = product.get()
            product_url = f"{base_url}/dp/{asin}"
            yield scrapy.Request(url=self.get_url(product_url), callback=self.parse_product_response, meta={'asin': asin})
        # To scrape all pages
        # next_page = response.xpath('//li[@class="a-last"]/a/@href').extract_first()
        # if next_page:
        #     url = base_url + next_page
        #     yield scrapy.Request(url=self.get_url(url), callback=self.parse_keyword_response)        


    def parse_product_response(self, response):
        seller_name = response.xpath('//*[@id="sellerProfileTriggerId"]/text()').extract_first()
        asin = response.meta['asin']
        seller_rank = response.xpath('//*[text()[contains(., "Best Sellers Rank")]]/parent::*//text()').extract()
        fba = response.xpath('//*[@class="tabular-buybox-text" and @tabular-attribute-name="Ships from"]/div/span/text()').extract_first()

        seller_id = response.xpath('//*[@id="merchantID"]/@value').extract_first()
        if seller_id:
            seller_url = f"{base_url}/sp?seller={seller_id}"
            yield scrapy.Request(url=self.get_url(seller_url),
                                callback=self.parse_seller_page,
                                meta={
                                        'SellerUrl': seller_url,
                                        'SellerName': seller_name,
                                        'asin': asin,
                                        'SellerRank': seller_rank,
                                        'FBA': fba
                                    })
        else:
            return



    def parse_seller_page(self, response):
        seller_url = response.meta['SellerUrl']
        seller_name = response.meta['SellerName']
        asin = response.meta['asin']
        seller_rank = response.meta['SellerRank']
        fba = response.meta['FBA']
        rating = response.xpath('//*[@id="feedback-summary-table"]/tbody/tr[2]/td[5]/span/text()').get()
        number_of_reviews = response.xpath('//*[@id="feedback-summary-table"]/tbody/tr[5]/td[5]/span/text()').get()
        
        x = response.xpath('//*[@id="feedback-summary-table"]/tbody/tr[2]/td[5]/span/text()')
        y = response.xpath('//*[@id="feedback-summary-table"]/tbody/tr[5]/td[5]/span/text()')

        print(response)
        print(x)
        print(y)
        print('hello')

        yield {
                'SellerUrl': seller_url,
                'SellerName': seller_name,
                'FBA': fba,
                'ASIN': asin,
                'Rating': rating,
                'NumberOfReviews': number_of_reviews,
                'SellerRank': seller_rank,
              }


    # def parse_product_page(self, response):
    #     seller_url = response.xpath('//*[@id="bylineInfo"]/@href').extract_first()
    #     seller_name = response.xpath('//*[@id="bylineInfo"]/text()').extract_first()
    #     asin = response.meta['asin']
    #     title = response.xpath('//*[@id="productTitle"]/text()').extract_first()
    #     seller_rank = response.xpath('//*[text()[contains(., "Best Sellers Rank")]]/parent::*//text()').extract()
    #     rating = response.xpath('//*[@id="acrPopover"]/@title').extract_first()
    #     number_of_reviews = response.xpath('//*[@id="acrCustomerReviewText"]/text()').extract_first()
    #     yield {'SellerUrl': seller_url, 'SellerName': seller_name, 'asin': asin, 'Title': title, 'Rating': rating, 'NumberOfReviews': number_of_reviews, 'SellerRank': seller_rank}

    
    def get_url(self, url):
        API_KEY = '603538f20599863705cc3bf82a543435'
        payload = {'api_key': API_KEY, 'url': url, 'country_code': 'au'}
        proxy_url = 'http://api.scraperapi.com/?' + urlencode(payload)
        return proxy_url