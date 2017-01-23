import scrapy
import writer
from find_licensor import find_licensor

if __name__ == "__main__":
    print("file is meant for import.")
    exit()


class IcdramaSe(scrapy.Spider):
    __domain = "icdrama.se"
    __protocol = "http"
    __baseURL = __protocol + "://" + __domain
    __timestamp = ""
    __clients = None

    name = __domain
    allowed_domains = [__domain]
    start_urls = [
        __baseURL + "/hk-drama/",
        __baseURL + "/hk-show/",
        __baseURL + "/hk-movie/",
        __baseURL + "/korean-drama/",
        __baseURL + "/korean-drama-cantonesedub/",
        __baseURL + "/korean-drama-chinesesubtitles/",
        __baseURL + "/korean-show/",
        __baseURL + "/chinese-drama/",
        __baseURL + "/chinese-drama-cantonesedub/",
        __baseURL + "/taiwanese-drama/",
        __baseURL + "/taiwanese-drama-cantonesedub/",
        __baseURL + "/japanese-drama/",
        __baseURL + "/japanese-drama-cantonesedub/",
        __baseURL + "/japanese-drama-chinesesubtitles/",
        __baseURL + "/movies/"
    ]

    def __init__(self, time_stamp, clients, **kwargs):
        self.__timestamp = time_stamp
        self.__clients = clients
        super(IcdramaSe, self).__init__(**kwargs)

    def parse(self, response):
        links = response.xpath('//a[@class="movie-image"]/@href').extract()
        for link in links:
            yield scrapy.Request(link, callback=self.parse_for_episodes)

        next_page = response.xpath('//span[@class="current"]/following::span/a/@href').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_for_episodes(self, response):
        links = response.xpath('//ul[@class="listep"]/li/a/@href').extract()
        for link in links:
            yield scrapy.Request(link, callback=self.parse_for_iframes)

    def parse_for_iframes(self, response):
        title = response.xpath('/html/head/title/text()').extract_first()
        links = response.xpath('//iframe[@id="iframeplayer"]/@src').extract()
        licensor = find_licensor(title, self.__clients)
        for link in links:
            writer.write("./debug/icdrama.se/" + self.__timestamp,
                         "./debug/icdrama.se/" + self.__timestamp + "/links.txt",
                         licensor + "<<@>>" + title + "<<@>>" + response.url + "<<@>>" + link)
