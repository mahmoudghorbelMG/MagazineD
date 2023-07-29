import scrapy
import csv

class CurrencySpider(scrapy.Spider):
    name = 'currency'
    allowed_domains = ['financialmodelingprep.com']
    start_urls = ['https://site.financialmodelingprep.com/currencies']

    def parse(self, response):
        currencies = response.xpath('//tbody/tr')
        for currency in currencies:

            name = currency.xpath('.//td[2]/text()').get()
            price = currency.xpath('.//td[3]/text()').get()
            change = currency.xpath('.//td[4]/text()').get()

            yield {
                'Name': name,
                                'Price': price,
                'Change': change
            }

