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
            if k == 'FBA':
                if 'Amazon' in v:
                    item[k] = 'yes'
                else:
                    item[k] = 'no'
            elif k == 'Rating':
                item[k] = v + '% Positive'
            elif k == 'SellerRank':
                string = " ".join([i.strip() for i in v if i.strip()])
                string = string.replace('Best Sellers Rank: ', '')
                string = string.replace('Best Sellers Rank ', '')
                item[k] = re.sub(r"\(([^\)]+)\)", ",", string)
                
        return item


