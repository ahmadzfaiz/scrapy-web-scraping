import scrapy
from books.items import BooksItem

class HumorBookSpider(scrapy.Spider):
    name = "humor_book"
    allowed_domains = ["books.toscrape.com", 'proxy.scrapeops.io']
    start_urls = ["https://books.toscrape.com"]

    custom_settings = {
        'FEEDS': {
            'output/humor_book.csv': {'format': 'csv'}
        },
        # 'ITEM_PIPELINES': {
        #     'books.pipelines.CleanBooksPipeline': 300
        # }
    }

    def parse(self, response):
        humor_book_url = response.css('div.side_categories ul li ul li ::attr(href)')[28].get()
        yield response.follow(url=humor_book_url, callback=self.parse_humor_book)

    def parse_humor_book(self, response):
        books = response.css('article.product_pod')
        data = BooksItem()

        for book in books:
            title = book.css('h3 a::attr(title)').get()
            price = book.css('p.price_color::text').get()
            rating = book.css('p.star-rating').attrib['class']
            
            data['title'] = title
            data['price'] = price
            data['rating'] = rating
            yield data

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(url=next_page, callback=self.parse_humor_book)
