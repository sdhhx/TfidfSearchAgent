# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import Request, FormRequest
from wooyun.items import WooyunItem
from scrapy.linkextractors import LinkExtractor

class WooyunSpder(scrapy.Spider):
	name = "wooyun"
	allowed_domains = ["wooyun.org"]
	#爬虫的起始地址
	start_urls = [
		"http://www.wooyun.org/bugs/new_public/"
	]
	
	#scrapy爬虫默认调用
	def parse(self,response):
		for n in range(1,2040):
			page = "/bugs/new_public/page/%d" %n
			url = response.urljoin(page)
			yield scrapy.Request(url, self.parse_title)
	
	#利用xpath表达式，抽取对应内容并省略
	def parse_title(self,response):
		item = WooyunItem()
		for info in response.xpath('//tbody/tr'):
			item['date'] = info.xpath('th/text()').extract()[0]
			item['url'] = "http://wooyun.org" + info.xpath('td/a/@href').extract()[0]
			item['title'] = info.xpath('td/a/text()').extract()[0]
			yield item