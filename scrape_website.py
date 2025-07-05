import scrapy
from scrapy.crawler import CrawlerProcess
from urllib.parse import urlparse, urljoin
import logging

class WebsiteSpider(scrapy.Spider):
    name = "website"

    def __init__(self, start_url=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = [start_url]
        self.allowed_domains = [urlparse(start_url).netloc]

    def parse(self, response):
        main = response.css('main') or response

        content_elements = main.css('p, li, pre, code, h1, h2, h3, h4, h5, h6')
        content = " ".join([el.get().strip() for el in content_elements.xpath("string()")])

        yield {
            "url": response.url,
            "title": main.css('h1::text').get(default="").strip(),
            "content": content,
        }

        # Crawl internal links
        for link in main.css('a::attr(href)').getall():
            full_url = urljoin(response.url, link)
            if full_url.startswith("http") and urlparse(full_url).netloc == self.allowed_domains[0]:
                yield response.follow(full_url, self.parse)

def scrape(start_url, output_file='output.json'):
    logging.getLogger("scrapy").setLevel(logging.CRITICAL)

    process = CrawlerProcess(settings={
        "FEEDS": {
            output_file: {
                "format": "json",
                "overwrite": True
            }
        },
        "ROBOTSTXT_OBEY": False,
        "DOWNLOAD_DELAY": 0.5,
        "DEPTH_LIMIT": 12,
        "CONCURRENT_REQUESTS": 16,
    })

    process.crawl(WebsiteSpider, start_url=start_url)
    process.start()
