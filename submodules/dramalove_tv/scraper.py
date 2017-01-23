import scrapy

import writer
from find_licensor import find_licensor
from report_structure import GenericReportRow

if __name__ == "__main__":
    print("file is meant for import.")
    exit()


class DramaloveTv(scrapy.Spider):
    __domain = "www.dramalove.tv"
    __protocol = "http"
    __baseURL = __protocol + "://" + __domain
    __timestamp = ""
    __clients = None

    name = __domain
    allowed_domains = [__domain, "k-vid.net", "k-vid.com"]
    start_urls = [
        __baseURL + "/dramas/",
        __baseURL + "/movies/",
        __baseURL + "/tvshows/",
    ]

    def __init__(self, time_stamp, clients, **kwargs):
        self.__timestamp = time_stamp
        self.__clients = clients
        super(DramaloveTv, self).__init__(**kwargs)

    def parse(self, response):
        pagination_link = response.xpath('//a[@class="next"]/@href').extract_first()
        if pagination_link is not None and pagination_link is not "":
            yield scrapy.Request(pagination_link, callback=self.parse)

        links = response.xpath('//a[contains(@class, "episode-type")]/@href').extract()
        for link in links:
            yield scrapy.Request(link, callback=self.parse_for_episodes)

    def parse_for_episodes(self, response):
        links = response.xpath('//a[@class="episode-link"]/@href').extract()
        for link in links:
            yield scrapy.Request(link, callback=self.parse_for_iframes)

    def parse_for_iframes(self, response):
        title = response.xpath('/html/head/title/text()').extract_first()
        licensor = find_licensor(title, self.__clients)
        iframe_tag_links = response.xpath('//div[@class="tab-content"]//iframe/@src').extract()
        video_tag_links = response.xpath('//div[@class="tab-content"]//video//source/@src').extract()

        for link in iframe_tag_links:
            if "k-vid.com" in link or "k-vid.net" in link:
                item = GenericReportRow()
                item['licensor_name'] = licensor
                item['site_pagetitle'] = title
                item['site_link'] = response.url
                yield scrapy.Request(link, callback=self.parse_for_kvid, meta={'item': item})
            else:
                writer.write("./debug/dramalove.tv/" + self.__timestamp,
                             "./debug/dramalove.tv/" + self.__timestamp + "/links.txt",
                             licensor + "<<@>>" + title + "<<@>>" + response.url + "<<@>>" + "nil" + "<<@>>" + link)
        for link in video_tag_links:
            writer.write("./debug/dramalove.tv/" + self.__timestamp,
                         "./debug/dramalove.tv/" + self.__timestamp + "/links.txt",
                         licensor + "<<@>>" + title + "<<@>>" + response.url + "<<@>>" + "nil" + "<<@>>" + link)

    def parse_for_kvid(self, response):
        video_tag_links = response.xpath('//div[@class="videocontent"]//video//source/@src').extract()
        for link in video_tag_links:
            writer.write("./debug/dramalove.tv/" + self.__timestamp,
                         "./debug/dramalove.tv/" + self.__timestamp + "/links.txt",
                         response.meta['item']['licensor_name'] + "<<@>>" +
                         response.meta['item']['site_pagetitle'] + "<<@>>" +
                         response.meta['item']['site_link'] + "<<@>>" + response.url + "<<@>>" + link)
