from typing import Any
import scrapy
from scrapy.http import Request, Response


class QuotesSpider(scrapy.Spider):
    name = "quotes"  

    def start_requests(self):
        self.logger.info('Starting request')
        url = 'https://quotes.toscrape.com/page/{page}/'
        n_pages = 10

        for page in range(1, n_pages + 1):
            self.logger.info(f'Getting details from page: {page}')
            yield Request(url=url.format(page=page), callback=self.parse_quote)

    def parse_quote(self, response):
        boxes = response.xpath('//div[@class="quote"]')

        for box in boxes:
            quote = box.xpath('./span/text()').get()
            author = box.xpath('.//small[@class="author"]/text()').get()
            tags = box.xpath('.//a[@class="tag"]/text()').getall()
            about = box.xpath('.//small[@class="author"]/following-sibling::a/@href').get()

            yield response.follow(
                url=response.urljoin(about), 
                meta={'qoute': quote, 'author': author, 'tags': tags},
                callback=self.parse_about
            )
            
    def parse_about(self, response):
        about = response.xpath('//div[@class="author-description"]/text()').get()
        about_born_date = response.xpath('//span[@class="author-born-date"]/text()').get()
        about_born_location = response.xpath('//span[@class="author-born-location"]/text()').get()
        yield {'quote': response.meta['qoute'], 'author': response.meta['author'], 
              'tags': response.meta['tags'], 'about': about, 'about_url': response.url, 
              'about_born_date': about_born_date, 'about_born_location': about_born_location}






        









        
                

