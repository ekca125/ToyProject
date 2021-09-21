# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CompanyItem(scrapy.Item):
    company_name = scrapy.Field()
    company_industry = scrapy.Field()
    company_year = scrapy.Field()
    company_class = scrapy.Field()
    company_employee = scrapy.Field()
    company_sales = scrapy.Field()

    average_star = scrapy.Field()
    salary_star = scrapy.Field()
    life_star = scrapy.Field()
    culture_star = scrapy.Field()
    opportunity_star = scrapy.Field()
    ceo_star = scrapy.Field()

    salary_고졸 = scrapy.Field()
    salary_대졸2 = scrapy.Field()
    salary_대졸4 = scrapy.Field()
    salary_주임 = scrapy.Field()
    salary_대리 = scrapy.Field()
    salary_과장 = scrapy.Field()
    salary_차장 = scrapy.Field()
