# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem

class SamplescraperPipeline(object):
    def process_item(self, item, spider):
        content = set()
        if item['text'] in content:
            DropItem('this quote exist')

        else:
            content.add(item['text'])
        return item
