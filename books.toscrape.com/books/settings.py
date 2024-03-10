# Scrapy settings for books project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import os
from dotenv import load_dotenv

load_dotenv()

BOT_NAME = "books"

SPIDER_MODULES = ["books.spiders"]
NEWSPIDER_MODULE = "books.spiders"

# Set Output Format
FEEDS = {
  'output/data.json': {'format': 'json'}
}

# PostgreSQL connection settings
PG_DATABASE = {
  'default': {
    'host': os.getenv('PG_HOST'), 
    'user': os.getenv('PG_USER'), 
    'password': os.getenv('PG_PASS'),  
    'dbname': os.getenv('PG_DB'),
    'port': os.getenv('PG_PORT')
  }
}

# ScrapeOps Settings as Middleware for User Agent and/or Browser Header
# See https://scrapeops.io/
SCRAPEOPS_API_KEY = os.getenv('SCRAPEOPS_API_KEY')
SCRAPEOPS_NUM_RESULTS = 5

SCRAPEOPS_FAKE_USER_AGENT_ENDPOINT = os.getenv('SCRAPEOPS_FAKE_USER_AGENT_ENDPOINT')
SCRAPEOPS_FAKE_USER_AGENT_ENABLED = True

SCRAPEOPS_FAKE_BROWSER_HEADER_ENDPOINT = os.getenv('SCRAPEOPS_FAKE_BROWSER_HEADER_ENDPOINT')
SCRAPEOPS_FAKE_BROWSER_HEADER_ENABLED = True

SCRAPEOPS_PROXY_ENABLED = True
SCRAPEOPS_PROXY_SETTINGS = {'country': 'jp'}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "books (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "books.middlewares.BooksSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
  # "books.middlewares.BooksDownloaderMiddleware": 543,
  'books.middlewares.ScrapeOpsFakeUserAgentMiddleware': 300,
  'books.middlewares.ScrapeOpsFakeBrowserHeaderAgentMiddleware': 300,

  # ScrapeOps IP Rotating
  'scrapeops_scrapy_proxy_sdk.scrapeops_scrapy_proxy_sdk.ScrapeOpsScrapyProxySdk': 725,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
  'books.pipelines.CleanBooksPipeline': 300,
  # 'books.pipelines.SaveToPostgresPipeline': 400,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
