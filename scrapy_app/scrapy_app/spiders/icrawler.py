# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class IcrawlerSpider(CrawlSpider):
    name = 'main'

    list_rules = {
        'css': {
            'citation-text': '.gs_fl > a:nth-child(3)::text',
            'citation-url': '.gs_fl > a:nth-child(3)::attr(href)',
            'journal-year-src': '.gs_a::text',
        },
        'xpath': {
            'url': '//h3[@class="gs_rt"]/a/@href',
            'title': '//h3[@class="gs_rt"]/a',
            'authors': '//div[@class="gs_a"]/a',
            'description': '//div[@class="gs_rs"]',
        }
    }

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

        obj = {}

        # URL
        obj['url'] = response.xpath(self.list_rules['xpath']['url']).extract()

        # Title
        title_list = []
        titles = response.xpath(self.list_rules['xpath']['title'])
        for item in titles:
            title = item.xpath('.//text()').extract()
            text = "".join(title)
            title_list.append(text)
        obj['title'] = title_list

        # citation-text
        obj['citation'] = response.css(self.list_rules['css']['citation-text']).extract()

        # citation-url
        obj['citation-url'] = response.css(self.list_rules['css']['citation-url']).extract()

        # authors
        author_list = []
        authors = response.xpath(self.list_rules['xpath']['authors'])
        for item in authors:
            title = item.xpath('.//text()').extract()
            text = "".join(title)
            author_list.append(text)
        obj['authors'] = author_list

        # description
        description_list = []
        description_text = response.xpath(self.list_rules['xpath']['description'])
        for item in description_text:
            title = item.xpath('.//text()').extract()
            text = "".join(title)
            description_list.append(text)
        obj['description'] = description_list

        # journal-year-src
        obj['journal-year-src'] = response.css(self.list_rules['css']['journal-year-src']).extract()

        return obj