import scrapy
import writer
from find_licensor import find_licensor
from report_structure import GenericReportRow
from string_utils import find_between

if __name__ == "__main__":
    print("file is meant for import.")
    exit()


class MyasiantvSe(scrapy.Spider):
    __domain = "myasiantv.se"
    __protocol = "http"
    __baseURL = __protocol + "://" + __domain
    __timestamp = ""
    __clients = None

    name = __domain
    allowed_domains = [__domain, "vidnow.to"]
    start_urls = [
        __baseURL + "/drama/", __baseURL + "/movie/"
    ]

    def __init__(self, time_stamp, clients, **kwargs):
        self.__timestamp = time_stamp
        self.__clients = clients
        super(MyasiantvSe, self).__init__(**kwargs)

    def parse(self, response):
        links = response.xpath("//*[@class='row']/div/a/@href").extract()
        next_page = response.xpath(
            "//ul[@class='pagination']/li[@class='current']/following-sibling::li/a/@href").extract_first()
        if next_page is not None and next_page is not "":
            yield scrapy.Request(next_page, callback=self.parse)

        for link in links:
            yield scrapy.Request(link, callback=self.parse_for_episodes)

    def parse_for_episodes(self, response):
        links = response.xpath('//ul[@class="list-episode"]/li/h2/a/@href').extract()
        for link in links:
            yield scrapy.Request(link, callback=self.parse_for_iframes)

    def parse_for_iframes(self, response):
        title = response.xpath('/html/head/title/text()').extract_first()
        links = response.xpath('//div[@id="player"]/iframe/@src').extract()
        licensor = find_licensor(title, self.__clients)
        for link in links:
            if "vidnow.to" in link:
                item = GenericReportRow()
                item['licensor_name'] = licensor
                item['site_pagetitle'] = title
                item['site_link'] = response.url
                yield scrapy.Request(link, callback=self.parse_for_vidnow, meta={'item': item})
            else:
                if link.startswith("//"):
                    link = "http:" + link
                    writer.write("./debug/myasiantv.se/" + self.__timestamp,
                                 "./debug/myasiantv.se/" + self.__timestamp + "/links.txt",
                                 licensor + "<<@>>" + title + "<<@>>" + response.url + "<<@>>" + link)

    def parse_for_vidnow(self, response):
        count = 0
        html = response.body
        while True:
            if count > 10:
                break
            result = find_between(html, "file: \"", "\",")
            if result is "":
                break
            writer.write("./debug/myasiantv.se/" + self.__timestamp,
                         "./debug/myasiantv.se/" + self.__timestamp + "/links.txt",
                         response.meta['item']['licensor_name'] + "<<@>>" +
                         response.meta['item']['site_pagetitle'] + "<<@>>" +
                         response.meta['item']['site_link'] + "<<@>>" + result)
            index = html.index("file: \"")
            html = html[index + len("file: \""):]
            count += 1
