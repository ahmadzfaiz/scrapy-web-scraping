import scrapy
from books.items import BookDetailsItem

class FantasyBookSpider(scrapy.Spider):
    name = "fantasy_book"
    allowed_domains = ["books.toscrape.com", 'proxy.scrapeops.io']
    start_urls = ["https://books.toscrape.com"]

    custom_settings = {
        'FEEDS': {
            'output/fantasy_book.csv': {'format': 'csv'}
        }
    }

    def parse(self, response):
        fantasy_book_url = response.css('div.side_categories ul li ul li ::attr(href)')[9].get()
        yield response.follow(url=fantasy_book_url, callback=self.parse_fantasy_book)

    def parse_fantasy_book(self, response):
        books = response.css('article.product_pod')

        for book in books:
            detail_url = book.css('h3 a::attr(href)').get()
            yield response.follow(url=detail_url, callback=self.parse_detail_fantasy_book)

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(url=next_page, callback=self.parse_fantasy_book)

    def parse_detail_fantasy_book(self, response):
        table = response.css('table tr')

        data = BookDetailsItem()
        data['id'] = table.css('td ::text')[0].get()
        data['product'] = table.css('td ::text')[1].get()
        data['price_incl_tax'] = table.css('td ::text')[2].get()
        data['price_excl_tax'] = table.css('td ::text')[3].get()
        data['tax'] = table.css('td ::text')[4].get()
        data['availability'] = table.css('td ::text')[5].get()
        data['review'] = table.css('td ::text')[6].get()
        data['description'] = response.xpath("//div[@id='product_description']/following-sibling::p/text()").get()

        yield data
        