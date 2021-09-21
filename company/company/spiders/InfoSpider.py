import os
import sys
from pathlib import Path

crawl_process_path = Path(os.getcwd())
print(crawl_process_path)
spider_path = crawl_process_path.joinpath("company").joinpath("spiders")
sys.path.append(spider_path.__str__())

from JobPlanetCompanyUrlAnalyzer import JobPlanetCompanyUrlAnalyzer
from JobPlanetStarAnalyzer import JobPlanetStarAnalyzer
from SaraminIndustryAnalyzer import SaraminIndustryAnalyzer
from SaraminInfoAnalyzer import SaraminInfoAnalyzer
from SaraminSalaryAnalyzer import SaraminSalaryAnalyzer
from items import *

import re
import datetime


def convert_dict_data_to_item_data(dict_data):
    company_item = CompanyItem()
    company_item['page'] = dict_data['page']
    company_item['crawl_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    company_item['company_name'] = dict_data['company_name']
    company_item['company_industry'] = dict_data['company_industry']
    company_item['company_year'] = dict_data['company_year']
    company_item['company_class'] = dict_data['company_class']
    company_item['company_employee'] = dict_data['company_employee']
    company_item['company_sales'] = dict_data['company_sales']

    company_item['average_star'] = dict_data['average_star']
    company_item['salary_star'] = dict_data['salary_star']
    company_item['life_star'] = dict_data['life_star']
    company_item['culture_star'] = dict_data['culture_star']
    company_item['opportunity_star'] = dict_data['opportunity_star']
    company_item['ceo_star'] = dict_data['ceo_star']
    company_item['salary_고졸'] = dict_data['salary_고졸']
    company_item['salary_대졸2'] = dict_data['salary_대졸2']
    company_item['salary_대졸4'] = dict_data['salary_대졸4']
    company_item['salary_주임'] = dict_data['salary_주임']
    company_item['salary_대리'] = dict_data['salary_대리']
    company_item['salary_과장'] = dict_data['salary_과장']
    company_item['salary_차장'] = dict_data['salary_차장']
    return company_item


class InfoSpider(scrapy.Spider):
    name = 'InfoSpider'

    def start_requests(self):
        company_page_url = 'https://www.saramin.co.kr/zf_user/' \
                           'company-search?searchWord=&area=&industry=31401&industry_kcode=21793&' \
                           'welfare=&scale=&listingType=&companyType=&employees=' \
                           '&revenue=&operatingRevenue=&netRevenue=&establishment=&salary=' \
                           '&startingSalary=&order=&recruitCheck=&page=$number$'
        for i in range(1, 101):
            company_info = {'page': i}
            request_url = company_page_url.replace("$number$", str(i))
            next_request = scrapy.Request(url=request_url, callback=self.parse_saramin_industry, errback=self.errback)
            next_request.cb_kwargs['prev_company_info'] = company_info
            yield next_request

    def parse_saramin_industry(self, response, prev_company_info):
        analyzer = SaraminIndustryAnalyzer(response.body)
        for request_url in analyzer.get_info():
            next_request = scrapy.Request(url=request_url, callback=self.parse_saramin_info, errback=self.errback)
            next_request.cb_kwargs['prev_company_info'] = prev_company_info
            yield next_request

    def parse_saramin_info(self, response, prev_company_info):
        analyzer = SaraminInfoAnalyzer(response.body)
        company_info = analyzer.get_base_info()
        company_info.update(prev_company_info)
        company_info.update(analyzer.get_info())
        #
        request_url = str(response.url).replace("view", "view-inner-salary")
        next_request = scrapy.Request(url=request_url, callback=self.parse_saramin_salary, errback=self.errback)
        next_request.cb_kwargs['prev_company_info'] = company_info
        yield next_request

    def parse_saramin_salary(self, response, prev_company_info):
        analyzer = SaraminSalaryAnalyzer(response.body)
        company_info = analyzer.get_base_info()
        company_info.update(prev_company_info)
        company_info.update(analyzer.get_info())

        url = 'https://www.jobplanet.co.kr/search?query=' + company_info["company_name"]
        url = re.sub(r'\([^)]*\)', '', url)
        next_request = scrapy.Request(url=url, callback=self.parse_job_planet_search, errback=self.errback)
        next_request.cb_kwargs['prev_company_info'] = company_info
        yield next_request

    def parse_job_planet_search(self, response, prev_company_info):
        analyzer = JobPlanetCompanyUrlAnalyzer(response.body)
        url = analyzer.get_info()
        url = url.replace("landing", "reviews")
        url = url.replace("premium_reviews", "reviews")
        url = url.replace("premium_reviews", "reviews")
        url = url.replace("info", "reviews")
        next_request = scrapy.Request(url=url, callback=self.parse_job_planet, errback=self.errback)
        next_request.cb_kwargs['prev_company_info'] = prev_company_info
        yield next_request

    def parse_job_planet(self, response, prev_company_info):
        analyzer = JobPlanetStarAnalyzer(response.body)
        company_info = analyzer.get_base_info()
        company_info.update(prev_company_info)
        company_info.update(analyzer.get_info())
        yield convert_dict_data_to_item_data(company_info)

    def errback(self, failure):
        print(f"oh no, failed to parse {failure.request}")
