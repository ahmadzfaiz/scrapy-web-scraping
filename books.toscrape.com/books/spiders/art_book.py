import scrapy
from books.items import BooksItem

class ArtBookSpider(scrapy.Spider):
    name = "art_book"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    custom_settings = {
        'FEEDS': {
            'output/art_book.csv': {'format': 'csv'}
        }
    }

    def parse(self, response):
        art_book_url = response.css('div.side_categories ul li ul li ::attr(href)')[23].get()
        yield response.follow(url=art_book_url, callback=self.parse_art_book)

    def parse_art_book(self, response):
        books = response.css('article.product_pod')
        data = BooksItem()

        for book in books:
            title = book.css('h3 a::attr(title)').get()
            price = book.css('p.price_color::text').get()
            
            data['title'] = title
            data['price'] = price
            yield data
