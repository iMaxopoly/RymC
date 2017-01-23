import scrapy
from scrapy import Field


class GenericReportRow(scrapy.Item):
    licensor_name = Field()
    site_pagetitle = Field()
    site_link = Field()
    cyberlocker_link = Field()
