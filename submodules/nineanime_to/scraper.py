import scrapy
import writer
from find_licensor import find_licensor

if __name__ == "__main__":
    print("file is meant for import.")
    exit()


class NineanimeTo(scrapy.Spider):
    __domain = "9anime.to"
    __protocol = "https"
    __baseURL = __protocol + "://" + __domain
    __timestamp = ""
    __clients = None

    name = __domain
    allowed_domains = [__domain]
    start_urls = [
        __baseURL + "/tv-series",
        __baseURL + "/movies",
        __baseURL + "/ova",
        __baseURL + "/ona",
        __baseURL + "/specials",
    ]
    download_delay = 2

    def __init__(self, time_stamp, clients, **kwargs):
        self.__timestamp = time_stamp
        self.__clients = clients
        super(NineanimeTo, self).__init__(**kwargs)

    def parse(self, response):
        links = response.xpath('//div[@class="item"]/a/@href').extract()
        for link in links:
            print link
        next_page_link = response.xpath(
            '//a[contains(@class, "btn") '
            'and contains(@class, "btn-lg") '
            'and contains(@class, "btn-primary") '
            'and contains(@class, "pull-right") '
            'and not(contains(@class, "disabled"))]/@href'
        ).extract_first()
        if next_page_link is None or next_page_link == "":
            return

        print "next page link", next_page_link
        yield scrapy.Request(response.urljoin(next_page_link), callback=self.parse)
