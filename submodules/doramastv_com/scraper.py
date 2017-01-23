import scrapy
import validators

import writer
from find_licensor import find_licensor
from report_structure import GenericReportRow

if __name__ == "__main__":
    print("file is meant for import.")
    exit()


class DoramastvCom(scrapy.Spider):
    __domain = "doramastv.com"
    __protocol = "http"
    __baseURL = __protocol + "://" + __domain
    __timestamp = ""
    __clients = None

    name = __domain
    allowed_domains = [__domain, "zet.videosxd.org"]
    start_urls = [
        __baseURL + "/lista-numeros",
        __baseURL + "/lista-A", __baseURL + "/lista-K",
        __baseURL + "/lista-B", __baseURL + "/lista-L",
        __baseURL + "/lista-C", __baseURL + "/lista-M",
        __baseURL + "/lista-D", __baseURL + "/lista-N",
        __baseURL + "/lista-E", __baseURL + "/lista-O",
        __baseURL + "/lista-F", __baseURL + "/lista-P",
        __baseURL + "/lista-G", __baseURL + "/lista-Q",
        __baseURL + "/lista-H", __baseURL + "/lista-R",
        __baseURL + "/lista-I", __baseURL + "/lista-S",
        __baseURL + "/lista-J", __baseURL + "/lista-T",
        __baseURL + "/lista-U", __baseURL + "/lista-V",
        __baseURL + "/lista-W", __baseURL + "/lista-X",
        __baseURL + "/lista-Y", __baseURL + "/lista-Z",
    ]

    def __init__(self, time_stamp, clients, **kwargs):
        self.__timestamp = time_stamp
        self.__clients = clients
        super(DoramastvCom, self).__init__(**kwargs)

    def parse(self, response):
        pagination_link = response.xpath('//a[@class="next"]/@href').extract_first()
        if pagination_link is not None and pagination_link is not "":
            yield scrapy.Request(response.urljoin(pagination_link), callback=self.parse)

        links = response.xpath('//div[@class="animes-bot"]/a/@href').extract()
        for link in links:
            yield scrapy.Request(response.urljoin(link), callback=self.parse_for_episodes)

    def parse_for_episodes(self, response):
        links = response.xpath('//ul[@id="lcholder"]//a/@href').extract()
        for link in links:
            yield scrapy.Request(response.urljoin(link), callback=self.parse_for_iframes)

    def parse_for_iframes(self, response):
        title = response.xpath('//title/text()').extract_first()
        licensor = find_licensor(title, self.__clients)
        third_party_links = response.xpath('//div[@class="tabitem"]/iframe/@src').extract()

        for link in third_party_links:
            item = GenericReportRow()
            item['licensor_name'] = licensor
            item['site_pagetitle'] = title.strip()
            item['site_link'] = response.url
            yield scrapy.Request(link, callback=self.parse_third_party, meta={'item': item})

    def parse_third_party(self, response):
        link = response.xpath("//iframe/@src").extract_first()
        if link is not None and validators.url(link, public=True):
            writer.write("./debug/doramastv.com/" + self.__timestamp,
                         "./debug/doramastv.com/" + self.__timestamp + "/links.txt",
                         response.meta['item']['licensor_name'] + "<<@>>" +
                         response.meta['item']['site_pagetitle'] + "<<@>>" +
                         response.meta['item']['site_link'] + "<<@>>" + link)
