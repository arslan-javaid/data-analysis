# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class IcrawlerSpider(CrawlSpider):
    name = 'main'

    def __init__(self, *args, **kwargs):
        # We are going to pass these args from our django view.
        # To make everything dynamic, we need to override them inside __init__ method
        # self.url = kwargs.get('url')
        # self.domain = kwargs.get('domain')
        # self.start_urls = [self.url]
        # self.allowed_domains = [self.domain]

        start_url = "https://scholar.google.com.pk/scholar?hl=en&as_sdt=0%2C5&q=erp+implementation&oq=ERP"


        self.domain = ["google.com"]
        self.allowed_domains = ["google.com"]
        self.url = [start_url]
        self.start_urls = [start_url]

        IcrawlerSpider.rules = [
            Rule(LinkExtractor(allow=("scholar\?.*")), callback='parse', follow=False),
        ]
        super(IcrawlerSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        # You can tweak each crawled page here
        # Don't forget to return an object.
        obj = {}
        obj['url'] = response.url

        # Title
        titleList = []
        titles = response.xpath('//h3[@class="gs_rt"]/a')
        for item in titles:
            title = item.xpath('.//text()').extract()
            h3 = "".join(title)
            titleList.append(h3)

        obj['title'] = titleList

        # yield {obj}
        return obj