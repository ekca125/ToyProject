from scrapy.crawler import *
from scrapy.utils.project import get_project_settings

from company.spiders.InfoSpider import InfoSpider

if __name__ == '__main__':
    process = CrawlerProcess(settings=get_project_settings())
    process.crawl(InfoSpider)
    process.start()
