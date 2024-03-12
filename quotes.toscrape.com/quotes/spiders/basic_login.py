import scrapy
from scrapy.http import FormRequest
from quotes.items import QuotesItem

class BasicLoginSpider(scrapy.Spider):
    name = "basic_login"
    # allowed_domains = ["quotes.toscrape.com"]
    # start_urls = ["https://quotes.toscrape.com"]

    def start_requests(self):
        login_url = 'https://quotes.toscrape.com/login'
        yield scrapy.Request(url=login_url, callback=self.login)

        # return FormRequest(login_url, formdata=login_data, callback=self.start_scraping)
    
    def login(self, response):
        token = response.css('input[name="csrf_token"] ::attr(value)').get()
        login_data = {
            'csrf_token': token,
            'username': 'johndoe',
            'password': 'foobar'
        }
        yield FormRequest.from_response(response, formdata=login_data, callback=self.start_scraping)

    def start_scraping(self, response):
        # Insert code to start scraping pages once logged in
        quotes = response.css('div.quote')
        data = QuotesItem()

        for quote in quotes:
            data['text'] = quote.css('span.text::text').get()
            data['author'] = quote.css('small.author::text').get()
            data['tags'] = quote.css('a.tag::text').getall()

            yield data

        # next_page = response.css('li.next a::attr(href)').get()
        # if next_page is not None:
        #     yield response.follow(url=next_page, callback=self.start_scraping)

