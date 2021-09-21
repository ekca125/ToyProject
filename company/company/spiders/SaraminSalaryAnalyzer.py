import re

from BaseAnalyzer import *


class SaraminSalaryAnalyzer(BaseAnalyzer):
    def __init__(self, response_body):
        super().__init__(response_body)
        self.response_soup = BeautifulSoup(response_body, 'html.parser')
        self.base_info = {
            'company_name': '',
            'salary_고졸': '',
            'salary_대졸2': '',
            'salary_대졸4': '',
            'salary_주임': '',
            'salary_대리': '',
            'salary_과장': '',
            'salary_차장': ''
        }

    def analyze(self):
        company_info = copy(self.base_info)
        name_tag = self.response_soup.find('h1', 'company_name').find('span', 'name')
        company_info['company_name'] = re.sub('[^ㄱ-ㅣ가-힣0-9A-Za-z()]+', '', name_tag.text)
        try:
            dl_tags = self.response_soup.find_all('dl', 'row')
            for dl_tag in dl_tags:
                title = str(dl_tag.find('dt').text)
                salary = re.sub('[^0-9]+', '', dl_tag.find('dd', 'index').text)
                if '4년' in title:
                    company_info["salary_대졸4"] = salary

                if '고졸' in title:
                    company_info["salary_고졸"] = salary
                elif '2,3년' in title:
                    company_info["salary_대졸2"] = salary
                elif '4년' in title:
                    company_info["salary_대졸4"] = salary
                elif '주임' in title:
                    company_info["salary_주임"] = salary
                elif '대리' in title:
                    company_info["salary_대리"] = salary
                elif '과장' in title:
                    company_info["salary_과장"] = salary
                elif '차장' in title:
                    company_info["salary_차장"] = salary
        except:
            pass
        return company_info
