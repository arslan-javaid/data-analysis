# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from time import sleep
import random


class TandfonlineSpider(scrapy.Spider):
    name = 'tandfonline'

    list_rules = {
        'xpath': {
            'url': '//div[@class="art_title"]/span/a/@href',
            'next-page': '//li[@class="pageLink-with-arrow"]/a/@href',

            'journal': '//div[@class="title-container"]/h1/a/text()',
            'title': '//h1/h1',
            'authors': '//a[@class="entryAuthor"]',
            'abstract': '//*[@class="article"]/div[1]/div[2]',
            'keywords': '//*[@class="article"]/div[2]',
            'citation': '//div[@class="value"]/text()',

        }
    }

    def __init__(self, *args, **kwargs):
        self.url = "https://www.tandfonline.com/action/doSearch?AllField=ERP+assimilation"
        self.start_urls = [self.url]

        self.domain = ["google.com"]
        self.allowed_domains = ["www.tandfonline.com"]

    def parse(self, response):

        # Process each URL
        urls = response.xpath(self.list_rules['xpath']['url']).extract()
        for url in urls:
            absolute_url = response.urljoin(url)
            yield Request(absolute_url, cookies={'store_language':'en'}, callback=self.parse_site)

        # Process next pages
        sleep(random.randrange(1, 3))
        next_page_url = response.xpath(self.list_rules['xpath']['next-page']).extract()
        next_page_url = next_page_url[1] if len(next_page_url) > 1 else next_page_url[0]
        absolute_next_url = response.urljoin(next_page_url)
        yield Request(absolute_next_url)

    def parse_site(self, response):
        # URL
        url = response.url

        # Journal
        journal = response.xpath(self.list_rules['xpath']['journal']).extract()

        # Title
        titles = self.get_complete_text(response.xpath(self.list_rules['xpath']['title']))

        # citation
        article_metrics =response.xpath(self.list_rules['xpath']['citation']).extract()
        views = article_metrics[0] if article_metrics else 0
        citation = article_metrics[1] if article_metrics else 0

        # authors
        authors = self.get_complete_text(response.xpath(self.list_rules['xpath']['authors']))

        # Abstract
        abstract = self.get_complete_text(response.xpath(self.list_rules['xpath']['abstract']))

        # Keywords
        keywords = self.get_complete_text(response.xpath(self.list_rules['xpath']['keywords']))

        yield {
            'url': url,
            'views': views.strip(' \t\n\r'),
            'citation': citation.strip(' \t\n\r'),
            'journal':  ''.join(journal).strip(' \t\n\r'),
            'title':  ''.join(titles).strip(' \t\n\r'),
            'author':  ''.join(authors).strip(' \t\n\r'),
            'abstract': ''.join(abstract).strip(' \t\n\r'),
            'keywords': ''.join(keywords).strip(' \t\n\r'),
        }

    def get_complete_text(self, html):
        text_list = []
        for element in html:
            item = element.xpath('.//text()').extract()
            text = "".join(item)
            text_list.append(text)

        return text_list
