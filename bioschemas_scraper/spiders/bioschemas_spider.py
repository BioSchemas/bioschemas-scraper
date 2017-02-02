from extruct.w3cmicrodata import MicrodataExtractor
import scrapy
from scrapy.spiders import CrawlSpider, Rule
import datetime


class BioschemasSpider(CrawlSpider):
    target_types = ['http://schema.org/Event']
    name = 'tess.elixir-europe_all'
    allowed_domains = ['tess.elixir-europe.org']
    start_urls = [
        'https://tess.elixir-europe.org/events?include_expired=true',
    ]

    custom_settings = {
        'ITEM_PIPELINES': {
            'bioschemas_scraper.pipelines.ElasticPipeline': 100
        }
    }

    def parse(self, response):
        mde = MicrodataExtractor()
        data = mde.extract(response.body)
        for item in data['items']:
            if item['type'] in self.target_types:
                item['indexed_date'] = datetime.date.today().isoformat()
                item['url'] = response.url
                yield item

        for url in response.xpath('//a/@href').extract():
            if '/events' in url:
                yield scrapy.Request(response.urljoin(url), callback=self.parse)


