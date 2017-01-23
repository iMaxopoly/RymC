import scrapy
import validators

import writer
from find_licensor import find_licensor
from report_structure import GenericReportRow
from string_utils import find_between

if __name__ == "__main__":
    print("file is meant for import.")
    exit()


class DramagoCom(scrapy.Spider):
    __domain = "www.dramago.com"
    __protocol = "http"
    __baseURL = __protocol + "://" + __domain
    __timestamp = ""
    __clients = None

    name = __domain
    allowed_domains = [__domain, "videozoo.me", "video66.org", "easyvideo.me", "playbb.me"]
    start_urls = [
        __baseURL + "/drama-shows",
        __baseURL + "/drama-movies",
    ]

    def __init__(self, time_stamp, clients, **kwargs):
        self.__timestamp = time_stamp
        self.__clients = clients
        super(DramagoCom, self).__init__(**kwargs)

    def parse(self, response):
        links = response.xpath('//table[@class="series_index"]//a/@href').extract()
        for link in links:
            yield scrapy.Request(response.urljoin(link), callback=self.parse_for_episodes)

    def parse_for_episodes(self, response):
        links = response.xpath('//div[@id="videos"]//a/@href').extract()
        for link in links:
            yield scrapy.Request(response.urljoin(link), callback=self.parse_for_partlist)

    def parse_for_partlist(self, response):
        links = response.xpath('//ul[@class="part_list"]//a/@href').extract()
        for link in links:
            yield scrapy.Request(response.urljoin(link), callback=self.parse_for_iframes)

    def parse_for_iframes(self, response):
        title = response.xpath('/html/head/title/text()').extract_first()
        links = response.xpath('//div[@class="vmargin"]//iframe/@src').extract()
        licensor = find_licensor(title, self.__clients)

        for link in links:
            if "videozoo.me" in link or "video66.org" in link or "easyvideo.me" in link or "playbb.me" in link:
                item = GenericReportRow()
                item['licensor_name'] = licensor
                item['site_pagetitle'] = title
                item['site_link'] = response.url
                yield scrapy.Request(link, callback=self.parse_deeper, meta={'item': item})

    def parse_deeper(self, response):
        html = response.body
        result = find_between(html, "url: 'h", "',")
        if result is "":
            return
        result = "h" + result
        if validators.url(result, public=True):
            writer.write("./debug/dramago.com/" + self.__timestamp,
                         "./debug/dramago.com/" + self.__timestamp + "/links.txt",
                         response.meta['item']['licensor_name'] + "<<@>>" +
                         response.meta['item']['site_pagetitle'] + "<<@>>" +
                         response.meta['item']['site_link'] + "<<@>>" + response.url + "<<@>>" + result)
