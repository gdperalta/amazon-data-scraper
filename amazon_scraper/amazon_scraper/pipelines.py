# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re


class AmazonScraperPipeline:
    def process_item(self, item, spider):
        for k, v in item.items():
            if not v:
                item[k] = ''  # replace empty list or None with empty string
                continue
            if k == 'Title':
                item[k] = v.strip()
            elif k == 'Rating':
                item[k] = v.replace(' out of 5 stars', '')
            elif k == 'SellerUrl':
                item[k] = 'https://www.amazon.com.au' + v
            elif k == 'SellerName':
                item[k] = v.replace('Visit the ', '')
            elif k == 'SellerRank':
                string = " ".join([i.strip() for i in v if i.strip()])
                new_string = string.replace('Best Sellers Rank: ', '')
                item[k] = re.sub(r"\(([^\)]+)\)", ",", new_string)
                
        return item


