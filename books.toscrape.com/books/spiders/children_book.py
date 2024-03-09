import scrapy
from books.items import BooksItem

class ChildrenBookSpider(scrapy.Spider):
    name = "children_book"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    custom_settings = {
        'FEEDS': {
            'output/children_book.csv': {'format': 'csv'}
        }
    }

    def parse(self, response):
        children_book_url = response.css('div.side_categories ul li ul li ::attr(href)')[9].get()
        yield response.follow(url=children_book_url, callback=self.parse_children_book)

    def parse_children_book(self, response):
        books = response.css('article.product_pod')
        data = BooksItem()

        for book in books:
            title = book.css('h3 a::attr(title)').get()
            price = book.css('p.price_color::text').get()
            
            data['title'] = title
            data['price'] = price
            yield data

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(url=next_page, callback=self.parse_children_book)
