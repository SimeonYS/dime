import re
import scrapy
from scrapy.loader import ItemLoader
from ..items import DimeItem
from itemloaders.processors import TakeFirst

pattern = r'(\xa0)?'

class DimeSpider(scrapy.Spider):
	name = 'dime'
	start_urls = ['https://www.dime-bank.com/About-Us/About-Dime-Bank/News']

	def parse(self, response):
		post_links = response.xpath('//a[@class="row"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		date = response.xpath('//span[@class="pr-date"]/text()').get()
		title = response.xpath('//div[@class="col-xs-12"]/h2/text()').get()
		content = response.xpath('//section[@class="zone details"]//div[@class="col-xs-12"]//text()[not (ancestor::h4 or ancestor::strong)]').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))

		item = ItemLoader(item=DimeItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		yield item.load_item()
