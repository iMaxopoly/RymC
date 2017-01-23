import scrapy
import writer
from find_licensor import find_licensor

if __name__ == "__main__":
    print("file is meant for import.")
    exit()


class DopekaCom(scrapy.Spider):
    __domain = "www.dopeka.com"
    __protocol = "http"
    __baseURL = __protocol + "://" + __domain
    __timestamp = ""
    __clients = None

    name = __domain
    allowed_domains = [__domain]
    start_urls = [
        __baseURL + "/doramas/"
    ]

    def __init__(self, time_stamp, clients, **kwargs):
        self.__timestamp = time_stamp
        self.__clients = clients
        super(DopekaCom, self).__init__(**kwargs)

    def parse(self, response):
        links = response.xpath(
            '//*[@id="menuzoneContent"]/ul/li[2]/ul/li/a/@href').extract()
        for link in links:
            yield scrapy.Request(response.urljoin(link), callback=self.parse_for_iframes)

    def parse_for_iframes(self, response):
        title = response.xpath('/html/head/title/text()').extract_first()
        links = response.xpath('//*[@class="rbcWidgetArea"]/iframe/@src').extract()
        licensor = find_licensor(title, self.__clients)

        pagination_links = response.xpath('//h1/a/@href').extract()
        for page_link in pagination_links:
            yield scrapy.Request(page_link, callback=self.parse_for_iframes)

        for link in links:
            if link.startswith("//"):
                link = "http:" + link
                writer.write("./debug/dopeka.com/" + self.__timestamp,
                             "./debug/dopeka.com/" + self.__timestamp + "/links.txt",
                             licensor + "<<@>>" + title + "<<@>>" + response.url + "<<@>>" + link)
