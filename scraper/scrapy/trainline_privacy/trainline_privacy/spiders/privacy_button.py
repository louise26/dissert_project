import scrapy

class PrivacyButtonSpider(scrapy.Spider):
    name = 'privacy_button'
    allowed_domains = ['www.ravelin.com']
    start_urls = ['http://www.ravelin.com/']

     #return all the links from the website and feed them to parse2
    def parse(self, response):
        privacy_link = response.xpath("//a[contains(@href, 'privacy')]")
        print(privacy_link)
        
       