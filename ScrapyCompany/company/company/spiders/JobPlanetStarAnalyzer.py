import re

from BaseAnalyzer import *


class JobPlanetStarAnalyzer(BaseAnalyzer):
    def __init__(self, response_body):
        super().__init__(response_body)
        self.base_info = {
            'average_star': -1.0,
            'salary_star': -1.0,
            'life_star': -1.0,
            'culture_star': -1.0,
            'opportunity_star': -1.0,
            'ceo_star': -1.0
        }

    def get_info(self):
        return self.analyze()

    def analyze(self):
        company_info = copy(self.base_info)

        stat_div = self.response_soup.find('div', 'stats_smr_sec')
        average_star_str = stat_div.find('span', 'rate_point').text
        company_info["average_star"] = float(average_star_str)

        txt_point_spans = stat_div.find_all("span", "txt_point")
        salary_star_str = str(txt_point_spans[0].text)
        life_star_str = txt_point_spans[1].text
        culture_star_str = txt_point_spans[2].text
        opportunity_star_str = txt_point_spans[3].text
        ceo_star_str = txt_point_spans[4].text

        salary_star_str = re.sub('[^0-9.]+', '', salary_star_str)
        life_star_str = re.sub('[^0-9.]+', '', life_star_str)
        culture_star_str = re.sub('[^0-9.]+', '', culture_star_str)
        opportunity_star_str = re.sub('[^0-9.]+', '', opportunity_star_str)
        ceo_star_str = re.sub('[^0-9.]+', '', ceo_star_str)

        company_info["salary_star"] = float(salary_star_str)
        company_info["life_star"] = float(life_star_str)
        company_info["culture_star"] = float(culture_star_str)
        company_info["opportunity_star"] = float(opportunity_star_str)
        company_info["ceo_star"] = float(ceo_star_str)
        return company_info


from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

if __name__ == '__main__':
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
