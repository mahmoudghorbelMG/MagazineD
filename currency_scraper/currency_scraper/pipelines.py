import csv

class CurrencyScraperPipeline:
    def open_spider(self, spider):
        self.file = open('currencies.csv', 'w', newline='')
        self.writer = csv.DictWriter(self.file, fieldnames=['Name', 'Price', 'Change'])
        self.writer.writeheader()

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        self.writer.writerow(item)
        return item
