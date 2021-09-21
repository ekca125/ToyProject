import re

from BaseAnalyzer import *


class SaraminInfoAnalyzer(BaseAnalyzer):
    def __init__(self, response_body):
        super().__init__(response_body)
        self.response_soup = BeautifulSoup(response_body, 'html.parser')
        self.base_info = {
            'company_name': '',
            'company_industry': '',
            'company_year': '',
            'company_class': '',
            'company_employee': '',
            'company_sales': ''
        }

    def analyze(self):
        company_info = copy(self.base_info)
        try:
            name_tag = self.response_soup.find('h1', 'company_name').find('span', 'name')
            company_info['company_name'] = re.sub('[^ㄱ-ㅣ가-힣0-9A-Za-z()]+', '', name_tag.text)

            industry_tag = self.response_soup.find('dl', 'info').find('dd')
            company_info['company_industry'] = re.sub('[^ㄱ-ㅣ가-힣0-9A-Za-z ]+', '', industry_tag.text)

            strong_tags = self.response_soup.find('ul', 'summary').find_all('strong')
            if len(strong_tags) < 4:
                raise IndexError
            company_info['company_year'] = re.sub('[^0-9]+', '', str(strong_tags[0].text).strip())
            company_info['company_class'] = re.sub('[^ㄱ-ㅣ가-힣0-9]+', '', str(strong_tags[1].text).strip())
            company_info['company_employee'] = re.sub('[^0-9]+', '', str(strong_tags[2].text).strip())
            company_info['company_sales'] = re.sub('[^0-9]+', '', str(strong_tags[3].text).strip())
        except IndexError:
            pass
        return company_info
