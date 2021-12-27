from abc import *

from bs4 import *

from copy import *


class BaseAnalyzer(metaclass=ABCMeta):
    def __init__(self, response_body):
        self.response_soup = BeautifulSoup(response_body, 'html.parser')
        self.base_info = {}

    def get_base_info(self):
        return self.base_info

    @abstractmethod
    def analyze(self):
        pass

    def get_info(self):
        try:
            return self.analyze()
        except:
            return self.base_info


'''
    BaseAnalyzer 은 HTML 을 분석하여 정보로 만드는 분석기 클래스들의 기본 클래스이다.
    변수
    response_soup : HTML 소스를 HTML 분석 라이브러리인 BeautifulSoup 에서 사용되는 Soup 타입으로 만든 변수이다.
    base_info : 분석된 결과값을 반환할때 사용되는 때에 사용되는 데이터의 정의이자 오류의 발생시에 반환되는 기본값이다.
    메소드(함수)
    analyze : HTML 을 분석하여 필요로하는 정보를 추출하고 base_info 에 기반하여 데이터를 반환하는 함수이다.
    get_info : analyze 의 오류 처리를 수행하여 분석 작업을 안정적으로 수행할 수 있도록 하는 함수이며 
    클래스를 사용할때 기본적으로 사용하는 것을 권장하는 함수이다.
'''

'''예상 진행도 SaraminIndustry -> SaraminInfo -> SaraminSalary -> JobPlanetCompanyUrlAnalyzer -> JobPlanetInfoAnalyzer(
JobPlanetStarAnalyzer) 
    
'''
