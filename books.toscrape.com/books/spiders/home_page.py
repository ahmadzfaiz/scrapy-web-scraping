import scrapy
from books.items import BooksItem


class HomePageSpider(scrapy.Spider):
    name = "home_page"
    allowed_domains = ["book.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    custom_settings = {
        'FEEDS': {
            'output/home_page.csv': {'format': 'csv'}
        }
    }

    def parse(self, response):
        books = response.css('article.product_pod')
        data = BooksItem()

        for book in books:
            title = book.css('h3 a::attr(title)').get()
            price = book.css('p.price_color::text').get()
            rating = book.css('p.star-rating').attrib['class']
            
            # yield {
            #     'title': title,
            #     'price': price,
            #     'rating': rating
            # }

            data['title'] = title
            data['price'] = price
            data['rating'] = rating
            yield data