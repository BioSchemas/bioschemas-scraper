from extruct.w3cmicrodata import MicrodataExtractor
import scrapy
from scrapy.spiders import SitemapSpider
import datetime


class BioschemasSpider(SitemapSpider):
    target_types = ['http://schema.org/Event']
    name = 'tess.elixir-europe_xml'
    sitemap_urls = ['https://tess.elixir-europe.org/sitemaps/events.xml']

    custom_settings = {
        'ITEM_PIPELINES': {
            'bioschemas_scrapper.pipelines.ElasticPipeline': 100
        }
    }

    def parse(self, response):
        mde = MicrodataExtractor()
        data = mde.extract(response.body)
        for item in data['items']:
            if item['type'] in self.target_types:
                record = {'indexed_date': datetime.date.today().isoformat(), 'url': response.url, 'body': item}
                yield record
