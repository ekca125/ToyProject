from BaseAnalyzer import *


class JobPlanetCompanyUrlAnalyzer(BaseAnalyzer):
    def __init__(self, response_body):
        super().__init__(response_body)
        self.base_info = None

    def analyze(self):
        company_card = self.response_soup.find("div", "result_company_card")
        url = "https://www.jobplanet.co.kr" + str(company_card.find("a")['href'])
        return url


'''
JobPlanetCompanyUrlAnalyzer는 잡플래닛에서 회사를 검색하고 그 결과가 나오는 웹페이지에서
가장 첫번째로 나오는(연관성이 높은) 회사의 정보가 들어있는 URL를 결과로 반환하는 클래스이다.

개선점
1. 웹페이지와 회사의 이름이 일치하지 않는 경우를 고려하여 잡플래닛의 회사이름도 같이 저장한다.
2. get_info는 base분석기에서 오류를 패스하도록 구성한다.
3. 별도의 데이터 함수를 만들어서 분석하도록 한다.
4. 데이터 셋을 정의한다. 이때 2의 함수에서 데이터가 없더라도 기본값을 반환하도록 만든다.

https://www.jobplanet.co.kr/search?query=%EB%B0%B0%EB%8B%AC%EC%9D%98%EB%AF%BC%EC%A
1%B1&category=search_new&search_keyword_hint_id=&_rs_con=seach&_rs_act=keyword_search


"" 로 나온다면 다음 값을 진행하지 않고 그냥 아이템을 반환해서 끝낸다.

'''
