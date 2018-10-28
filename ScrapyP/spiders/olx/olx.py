# -*- coding: utf-8 -*-
import re
import scrapy
from scrapy import Request
from scrapy import Item


class OlxSpider(scrapy.Spider):
    name = 'olx'
    allowed_domains = ['olx.com.pk']
    start_urls = ['https://www.olx.com.pk/property-for-sale/categories/',
                  'https://www.olx.com.pk/property-for-rent/categories/',
                  'https://www.olx.com.pk/vehicles/categories/',
                  'https://www.olx.com.pk/bikes/categories/',
                  'https://www.olx.com.pk/electronics-home-appliances/categories/',
                  'https://www.olx.com.pk/furniture-home-decor/categories/',
                  'https://www.olx.com.pk/business-industrial-agriculture/categories/',
                  'https://www.olx.com.pk/services/categories/',
                  'https://www.olx.com.pk/mobiles-tablets/categories/',
                  'https://www.olx.com.pk/animals/categories/',
                  'https://www.olx.com.pk/books-sports-hobbies/categories/',
                  'https://www.olx.com.pk/fashion-beauty/categories/',
                  'https://www.olx.com.pk/kids-baby-products/categories/']
    custom_settings = {
        'DOWNLOAD_DELAY': 7,
        'ROBOTSTXT_OBEY': False,
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36'
    }

    def parse(self, response):
        for url in self.get_cats(response):
            yield Request(url=url, callback=self.parse_listing)

    def parse_listing(self, response):

        for url in self.get_all_pages(response):
            yield Request(url=url, callback=self.parse_listing)

        for url in self.get_items_urls(response):
            yield Request(url=url, callback=self.parse_item,
                          meta={'cat': self.get_category(response)})

    def parse_item(self, response):
        l = DataItem()
        cleaned = self._clean_in(response.css('.show-map-link::text').extract())
        l['phone_no'] = '0{}'.format(response.css('.fnormal::text').extract_first())
        l['name'] = response.css('.userdetails span::text').extract_first()
        l['location'] = ' '.join(cleaned)
        l['category'] = response.meta['cat']
        yield l

    def get_cats(self, response):
        return response.css('.link-relatedcategory::attr(href)').extract()

    def get_items_urls(self, response):
        return response.css('.lpv-item-link::attr(href)').extract()

    def get_category(self, response):
        return response.css('.breadcrumb li h1::text').extract_first()

    def get_all_pages(self, response):
        return response.css('.pager span a::attr(href)').extract()

    def _clean_in(self, values):
        values = [re.sub('\W+', ' ', x).strip() for x in values if x]
        return [x for x in values if x]


class DataItem(Item):
    id = scrapy.Field()
    name = scrapy.Field()
    phone_no = scrapy.Field()
    category = scrapy.Field()
    location = scrapy.Field()
