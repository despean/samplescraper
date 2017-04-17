# -*- coding: utf-8 -*-
import scrapy
from ..items import SamplescraperItem


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        items = SamplescraperItem()
        for q in response.css('body > div > div:nth-child(2) > div.col-md-8 > div'):
            items['text'] = q.css('span.text::text').extract_first()
            items['author'] = q.css('span:nth-child(2) > small::text').extract_first()
            url = q.css('span > a::attr(href)').extract_first()
            if url:
                url = response.urljoin(url)
                request = scrapy.Request(url=url, callback=self.author_details, dont_filter=False)
                request.meta['items'] = items
                yield request
        next_page = response.css('li.next > a::attr(href)').extract_first()
        if next_page:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(url=next_page, callback=self.parse)

    def author_details(self, response):
        items = response.request.meta['items']

        items['date_birth'] = response.css(
            'body > div > div.author-details > p:nth-child(2) > span.author-born-date::text').extract_first()
        items['Location'] = response.css(
            'body > div > div.author-details > p:nth-child(2) > span.author-born-location::text').extract_first()
        yield items
