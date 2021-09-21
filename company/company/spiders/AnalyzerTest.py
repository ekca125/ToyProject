import unittest

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from JobPlanetCompanyUrlAnalyzer import JobPlanetCompanyUrlAnalyzer
from SaraminIndustryAnalyzer import SaraminIndustryAnalyzer
from SaraminInfoAnalyzer import SaraminInfoAnalyzer
from SaraminSalaryAnalyzer import SaraminSalaryAnalyzer
from JobPlanetStarAnalyzer import JobPlanetStarAnalyzer

import re


class MyTestCase(unittest.TestCase):
    '''
    def test_analyze_saramin_industry(self):
        driver = webdriver.Remote('http://127.0.0.1:4444/wd/hub', DesiredCapabilities.CHROME)
        company_page_url = 'https://www.saramin.co.kr/zf_user/company-search?page=$number$&searchWord=&ind_key%5B' \
                           '%5D=30118 '
        driver.get(company_page_url.replace('$number$', "1"))
        driver.implicitly_wait(10)
        result_info = SaraminIndustryAnalyzer(driver.page_source).get_info()
        driver.quit()
        print(result_info)

    def test_analyze_saramin_info(self):
        driver = webdriver.Remote('http://127.0.0.1:4444/wd/hub', DesiredCapabilities.CHROME)
        url = 'https://www.saramin.co.kr/zf_user/company-info/view?csn=RVVRNUtxblVZU08waUlEU0ZSVlVxdz09'
        driver.get(url)
        driver.implicitly_wait(10)
        result_info = SaraminInfoAnalyzer(driver.page_source).get_info()
        driver.quit()
        print(result_info)

    def test_analyze_saramin_salary(self):
        driver = webdriver.Remote('http://127.0.0.1:4444/wd/hub', DesiredCapabilities.CHROME)
        url = 'https://www.saramin.co.kr/zf_user/company-info/view-inner-salary?csn=RVVRNUtxblVZU08waUlEU0ZSVlVxdz09'
        driver.get(url)
        driver.implicitly_wait(10)
        result_info = SaraminSalaryAnalyzer(driver.page_source).get_info()
        driver.quit()
        print(result_info)
    '''

    def test_analyze_job_planet_company_url(self):
        url = 'https://www.jobplanet.co.kr/search?query=' \
              + re.sub("[^ㄱ-ㅣ가-힣0-9A-Za-z(.*)]+", "", '(주)카카오엔터테인먼트')
        driver = webdriver.Remote('http://127.0.0.1:4444/wd/hub', DesiredCapabilities.CHROME)
        driver.get(url)
        # driver.implicitly_wait(10)
        result_info = JobPlanetCompanyUrlAnalyzer(driver.page_source).get_info()
        driver.quit()
        print(result_info)

    '''
    def test_analyze_job_planet_company_star(self):
        url = 'https://www.jobplanet.co.kr/companies/50181/' \
              'reviews/%EC%B9%B4%EC%B9%B4%EC%98%A4%EC%97%94%ED%84%B0%ED%85%8C%EC%9D%B8%EB%A8%BC%ED%8A%B8'
        driver = webdriver.Remote('http://127.0.0.1:4444/wd/hub', DesiredCapabilities.CHROME)
        driver.get(url)
        driver.implicitly_wait(10)
        driver.get(url)
        driver.implicitly_wait(10)
        result_info = JobPlanetStarAnalyzer(driver.page_source).get_info()
        driver.quit()
        print(result_info)
    '''


if __name__ == '__main__':
    unittest.main()
