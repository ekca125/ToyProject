from BaseAnalyzer import *


class SaraminIndustryAnalyzer(BaseAnalyzer):
    def __init__(self, response_body):
        super().__init__(response_body)
        self.prefix_url = 'https://www.saramin.co.kr'
        self.base_info = []

    def analyze(self):
        urls = copy(self.base_info)
        company_info_blocks = self.response_soup.find_all('div', 'company_info')
        for company_info_block in company_info_blocks:
            company_info_block_soup = BeautifulSoup(str(company_info_block), 'html.parser')
            company_info_div = company_info_block_soup.find("div", "company_info").find("a")
            urls.append(self.prefix_url + str(company_info_div["href"]))
        return urls
