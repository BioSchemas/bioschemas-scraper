# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from elasticsearch import Elasticsearch
from scrapy.exceptions import DropItem
from utils.validators import validate_item


class BioschemasSpiderPipeline(object):
    def process_item(self, item, spider):
        return item


class ElasticPipeline(object):

    def __init__(self, elastic_host, elastic_port, index_name):
        self.elastic_host = elastic_host
        self.elastic_port = elastic_port
        self.index_name = index_name
        self.elastic_client = Elasticsearch([{'host': self.elastic_host, 'port': self.elastic_port}])
        self.processed = []

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            elastic_host=crawler.settings.get('ELASTIC_HOST'),
            elastic_port=crawler.settings.get('ELASTIC_PORT'),
            index_name=crawler.spider.name
        )

    def process_item(self, item, spider):
        if item not in self.processed:
            item['validation'] = validate_item(item['body'])
            self.elastic_client.index(index=self.index_name, doc_type=item['body']['type'], body=item)
            self.processed.append(item)
        else:
            raise DropItem("Duplicate item found: %s" % item)
        return item
