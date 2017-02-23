import scrapy
import writer
from find_licensor import find_licensor
from report_structure import GenericReportRow
from string_utils import find_between

if __name__ == "__main__":
    print("file is meant for import.")
    exit()


class EstrenosdoramasNet(scrapy.Spider):
    __domain = "www.estrenosdoramas.net"
    __protocol = "http"
    __baseURL = __protocol + "://" + __domain
    __timestamp = ""
    __clients = None

    name = __domain
    allowed_domains = [__domain, "mundoasia.net"]
    start_urls = [
        __baseURL + "/category/a", __baseURL + "/category/h",
        __baseURL + "/category/b", __baseURL + "/category/i",
        __baseURL + "/category/c", __baseURL + "/category/j",
        __baseURL + "/category/d", __baseURL + "/category/k",
        __baseURL + "/category/e", __baseURL + "/category/l",
        __baseURL + "/category/f", __baseURL + "/category/m",
        __baseURL + "/category/g", __baseURL + "/category/n",
        __baseURL + "/category/o", __baseURL + "/category/u",
        __baseURL + "/category/p", __baseURL + "/category/v",
        __baseURL + "/category/q", __baseURL + "/category/w",
        __baseURL + "/category/r", __baseURL + "/category/x",
        __baseURL + "/category/s", __baseURL + "/category/y",
        __baseURL + "/category/t", __baseURL + "/category/z"
    ]

    def __init__(self, time_stamp, clients, **kwargs):
        self.__timestamp = time_stamp
        self.__clients = clients
        super(EstrenosdoramasNet, self).__init__(**kwargs)

    def parse(self, response):
        links = response.xpath(
            "//*[@id='main-wrapper']/div[1]/div/div/a/@href").extract()
        for link in links:
            yield scrapy.Request(link, callback=self.parse_for_episodes)

    def parse_for_episodes(self, response):
        links = response.xpath('//*[@id="lcp_instance_0"]/li/a/@href').extract()
        for link in links:
            yield scrapy.Request(link, callback=self.parse_for_iframes)

    def parse_for_iframes(self, response):
        title = response.xpath('/html/head/title/text()').extract_first()
        links = response.xpath('//*[@class="tab_container"]/div/p/iframe/@src').extract()
        licensor = find_licensor(title, self.__clients)
        for link in links:
            if "mundoasia.net" in link:
                item = GenericReportRow()
                item['licensor_name'] = licensor
                item['site_pagetitle'] = title
                item['site_link'] = response.url
                yield scrapy.Request(link, callback=self.parse_for_mundoasia, meta={'item': item})
            else:
                if link.startswith("//"):
                    link = "http:" + link
                    writer.write("./debug/estrenosdoramas.net/" + self.__timestamp,
                                 "./debug/estrenosdoramas.net/" + self.__timestamp + "/links.txt",
                                 licensor + "<<@>>" + title + "<<@>>" + response.url + "<<@>>" + link)
                else:
                    writer.write("./debug/estrenosdoramas.net/" + self.__timestamp,
                                 "./debug/estrenosdoramas.net/" + self.__timestamp + "/links.txt",
                                 licensor + "<<@>>" + title + "<<@>>" + response.url + "<<@>>" + link)

    def parse_for_mundoasia(self, response):
        count = 0
        html = response.body
        while True:
            if count > 10:
                break
            result = find_between(html, "{file:'", "',label")
            if result is "":
                break
            writer.write("./debug/estrenosdoramas.net/" + self.__timestamp,
                         "./debug/estrenosdoramas.net/" + self.__timestamp + "/links.txt",
                         response.meta['item']['licensor_name'] + "<<@>>" +
                         response.meta['item']['site_pagetitle'] + "<<@>>" +
                         response.meta['item']['site_link'] + "<<@>>" + result)
            index = html.index("{file:'")
            html = html[index + len("{file:'"):]
            count += 1
