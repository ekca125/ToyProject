# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import time

from scrapy import signals

# useful for handling different item types with a single interface

from scrapy.http import HtmlResponse
from scrapy.utils.python import to_bytes
# useful for handling different item types with a single interface

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from nordvpn_switcher import initialize_VPN, rotate_VPN, terminate_VPN


class SeleniumMiddleware(object):

    def __init__(self):
        self.driver = None
        # 25회 요청후에 VPN 변경 요청
        self.current_request_number = 0
        self.change_request_number = 25
        # VPN init 설정
        self.settings = initialize_VPN()

    @classmethod
    def from_crawler(cls, crawler):
        middleware = cls()
        crawler.signals.connect(middleware.spider_opened, signals.spider_opened)
        crawler.signals.connect(middleware.spider_closed, signals.spider_closed)
        return middleware

    def spider_opened(self, spider):
        chrome_driver = "C:\\data\\SeleniumDriver\\chromedriver.exe"
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        self.driver = webdriver.Chrome(chrome_driver, options=chrome_options)
        self.driver.set_page_load_timeout(60)

    def spider_closed(self, spider):
        self.driver.quit()

    def check_and_rotate_vpn(self):
        # 일정 요청 회차마다 VPN의 IP 변경
        self.current_request_number += 1
        if self.current_request_number >= self.change_request_number:
            rotate_VPN(self.settings)
            self.current_request_number = 0

    def force_rotate_vpn(self):
        # 강제로 VPN IP 변경
        rotate_VPN(self.settings)
        self.current_request_number = 0

    def process_request(self, request, spider):
        self.request_and_response_with_safe_depth(request, 2)
        body = to_bytes(text=self.driver.page_source)
        return HtmlResponse(url=request.url, body=body, encoding='utf-8', request=request)

    def request_and_response_with_safe_depth(self, request, depth):
        assert self.driver is not None
        self.check_and_rotate_vpn()
        try:
            self.driver_get_url(request)
        except TimeoutError:
            if depth <= 0:
                raise TimeoutError
            else:
                self.force_rotate_vpn()
                self.request_and_response_with_safe_depth(request, depth - 1)

    def driver_get_url(self, request):
        self.driver.get(request.url)
        self.driver.implicitly_wait(10)
        if "jobplanet" in request.url and "query" in request.url:
            pass
        elif "jobplanet" in request.url:
            self.driver.get(request.url)
            wait = WebDriverWait(self.driver, 120)
            element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "rate_point")))


class CompanySpiderMiddleware:
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

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class CompanyDownloaderMiddleware:
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
        spider.logger.info('Spider opened: %s' % spider.name)
