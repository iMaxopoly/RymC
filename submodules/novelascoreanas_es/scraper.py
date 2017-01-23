import scrapy
import writer
from find_licensor import find_licensor
from report_structure import GenericReportRow
from string_utils import find_between

if __name__ == "__main__":
    print("file is meant for import.")
    exit()


class NovelascoreanasEs(scrapy.Spider):
    __domain = "www.novelascoreanas.es"
    __protocol = "http"
    __baseURL = __protocol + "://" + __domain
    __timestamp = ""
    __clients = None

    name = __domain
    allowed_domains = [__domain, "ww2.peliculasm.tv", "reproductor.novelascoreanas.es"]
    start_urls = [
        __baseURL + "/letra/a/", __baseURL + "/letra/h/",
        __baseURL + "/letra/b/", __baseURL + "/letra/i/",
        __baseURL + "/letra/c/", __baseURL + "/letra/j/",
        __baseURL + "/letra/d/", __baseURL + "/letra/k/",
        __baseURL + "/letra/e/", __baseURL + "/letra/l/",
        __baseURL + "/letra/f/", __baseURL + "/letra/m/",
        __baseURL + "/letra/g/", __baseURL + "/letra/n/",
        __baseURL + "/letra/o/", __baseURL + "/letra/u/",
        __baseURL + "/letra/p/", __baseURL + "/letra/v/",
        __baseURL + "/letra/q/", __baseURL + "/letra/w/",
        __baseURL + "/letra/r/", __baseURL + "/letra/x/",
        __baseURL + "/letra/s/", __baseURL + "/letra/y/",
        __baseURL + "/letra/t/", __baseURL + "/letra/z/",
        __baseURL + "/letra/1/"
    ]

    def __init__(self, time_stamp, clients, **kwargs):
        self.__timestamp = time_stamp
        self.__clients = clients
        super(NovelascoreanasEs, self).__init__(**kwargs)

    def parse(self, response):
        links = response.xpath(
            "//div[contains(@class, 'boxgrid') and contains(@class, 'captionfull')]/a/@href").extract()
        for link in links:
            yield scrapy.Request(response.urljoin(link), callback=self.parse_for_episodes)

    def parse_for_episodes(self, response):
        links = response.xpath('//*[@id="Cols"]/div/a/@href').extract()
        for link in links:
            if "trailer" in link.lower():
                continue
            yield scrapy.Request(response.urljoin(link), callback=self.parse_for_iframes)

    def parse_for_iframes(self, response):
        title = response.xpath('/html/head/title/text()').extract_first()
        links = response.xpath('//*[@id="repros"]/center/iframe/@src').extract()
        licensor = find_licensor(title, self.__clients)
        for link in links:
            if "reproductor.novelascoreanas.es" in link:
                item = GenericReportRow()
                item['licensor_name'] = licensor
                item['site_pagetitle'] = title
                item['site_link'] = response.url
                link_index = link.index("reproductor.novelascoreanas.es")
                link = "http://" + link[link_index:]
                yield scrapy.Request(link, callback=self.parse_for_reproductor, meta={'item': item})
            else:
                if link.startswith("//"):
                    link = "http:" + link
                writer.write("./debug/novelascoreanas.es/" + self.__timestamp,
                             "./debug/novelascoreanas.es/" + self.__timestamp + "/links.txt",
                             licensor + "<<@>>" + title + "<<@>>" + response.url + "<<@>>" + link)

    def parse_for_reproductor(self, response):
        iframe_src = response.xpath('/html/body/iframe/@src').extract_first()
        if "peliculasm.tv" in iframe_src:
            yield scrapy.Request(iframe_src, callback=self.parse_for_peliculasm, meta={'item': response.meta['item']})
        else:
            if iframe_src.startswith("//"):
                iframe_src = "http:" + iframe_src
            writer.write("./debug/novelascoreanas.es/" + self.__timestamp,
                         "./debug/novelascoreanas.es/" + self.__timestamp + "/links.txt",
                         response.meta['item']['licensor_name'] + "<<@>>" +
                         response.meta['item']['site_pagetitle'] + "<<@>>" +
                         response.meta['item']['site_link'] + "<<@>>" + iframe_src)

    def parse_for_peliculasm(self, response):
        count = 0
        html = response.body
        while True:
            if count > 10:
                break
            result = find_between(html, "{file:'", "',label")
            if result is "":
                break
            writer.write("./debug/novelascoreanas.es/" + self.__timestamp,
                         "./debug/novelascoreanas.es/" + self.__timestamp + "/links.txt",
                         response.meta['item']['licensor_name'] + "<<@>>" +
                         response.meta['item']['site_pagetitle'] + "<<@>>" +
                         response.meta['item']['site_link'] + "<<@>>" + result)
            index = html.index("{file:'")
            html = html[index + len("{file:'"):]
            count += 1
