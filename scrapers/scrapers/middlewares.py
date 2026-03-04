# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from urllib.parse import urlencode
from random import randint
import requests
import logging
import os
from dotenv import load_dotenv

load_dotenv()

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class ScrapersSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    async def process_start(self, start):
        # Called with an async iterator over the spider start() method or the
        # matching method of an earlier spider middleware.
        async for item_or_request in start:
            yield item_or_request

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class ScrapersDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class ScrapeOpsFakeBrowserHeaderAgentMiddleware:

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def __init__(self, settings):
        self.scrapeops_api_key = os.getenv("SCRAPEOPS_API_KEY")
        self.scrapeops_endpoint = settings.get('SCRAPEOPS_FAKE_BROWSER_HEADER_ENDPOINT', 'http://headers.scrapeops.io/v1/browser-headers')
        self.scrapeops_fake_browser_headers_active = settings.get('SCRAPEOPS_FAKE_BROWSER_HEADER_ENABLED', False)
        self.scrapeops_num_results = settings.get('SCRAPEOPS_NUM_RESULTS')
        self.headers_list = []
        self.logger = logging.getLogger(__name__)
        if self.scrapeops_fake_browser_headers_active:
            self._get_headers_list()
        self._validate_active_state()

    def _get_headers_list(self):
        if not self.scrapeops_api_key:
            self.logger.error("SCRAPEOPS_API_KEY not detected, middleware will shut down.")
            self.scrapeops_fake_browser_headers_active = False
            return

        payload = {'api_key': self.scrapeops_api_key}
        if self.scrapeops_num_results is not None:
            payload['num_results'] = self.scrapeops_num_results
        try:
            response = requests.get(self.scrapeops_endpoint, params=urlencode(payload), timeout=5)
            response.raise_for_status()
            json_response = response.json()
            self.headers_list = json_response.get('result', [])
            if not self.headers_list:
                self.logger.warning("ScrapeOps returned empty list.")
        except Exception as e:
            self.logger.error(f"Error occurred while trying to get headers from ScrapeOps: {e}")
            self.headers_list = []
            self.scrapeops_fake_browser_headers_active = False

    def _validate_active_state(self):
        if (not self.scrapeops_api_key or
            not self.scrapeops_fake_browser_headers_active or
            not self.headers_list):
            self.scrapeops_fake_browser_headers_active = False

    def _get_random_browser_header(self):
        if not self.headers_list:
            return {}
        random_index = randint(0, len(self.headers_list) - 1)
        return self.headers_list[random_index]

    def process_request(self, request, spider):
        if not self.scrapeops_fake_browser_headers_active:
            return

        random_browser_header = self._get_random_browser_header()
        if not random_browser_header:
            return

        request.headers.update(random_browser_header)
        self.logger.debug(f"New Headers: {random_browser_header}")