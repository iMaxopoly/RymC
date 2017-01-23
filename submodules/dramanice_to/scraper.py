import cfscrape
import scrapy

import writer
from find_licensor import find_licensor
from report_structure import GenericReportRow

if __name__ == "__main__":
    print("file is meant for import.")
    exit()


class DramaniceTo(scrapy.Spider):
    __domain = "www1.dramanice.to"
    __protocol = "http"
    __baseURL = __protocol + "://" + __domain
    __timestamp = ""
    __clients = None

    name = __domain
    allowed_domains = [__domain, "k-vid.net", "k-vid.com"]
    start_urls = [
        __baseURL + "/list-all-drama",
    ]

    def __init__(self, time_stamp, clients, **kwargs):
        self.__timestamp = time_stamp
        self.__clients = clients
        super(DramaniceTo, self).__init__(**kwargs)

    def start_requests(self):
        cf_requests = []
        for url in self.start_urls:
            token, agent = cfscrape.get_tokens(
                url, "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 "
                     "Safari/537.36")
            cf_requests.append(scrapy.Request(url=url,
                                              cookies=token,
                                              headers={'User-Agent': agent}))
        return cf_requests

    def parse(self, response):
        links = response.xpath('//div[@class="drama_list_body"]//a/@href').extract()
        for link in links:
            yield scrapy.Request(response.urljoin(link), callback=self.parse_for_all_episode_links)

    def parse_for_all_episode_links(self, response):
        rel = response.xpath('//a[@id="view_more_episodes"]/@rel').extract_first()
        str_alias = response.xpath('//a[@id="view_more_episodes"]/@str-alias').extract_first()
        if rel is None or str_alias is None or rel is "" or str_alias is "":
            return
        yield scrapy.Request(self.__baseURL + "/load-episode.html?id={}&str={}".format(rel, str_alias),
                             callback=self.parse_collect_episode_links)

    def parse_collect_episode_links(self, response):
        links = response.xpath('//ul[@class="list_episode"]//a/@href').extract()
        for link in links:
            yield scrapy.Request(response.urljoin(link), callback=self.parse_for_iframes)

    def parse_for_iframes(self, response):
        title = response.xpath('/html/head/title/text()').extract_first()
        licensor = find_licensor(title, self.__clients)
        links = response.xpath('//div[@class="anime_muti_link"]//a/@data-video').extract()
        for link in links:
            if "k-vid.com" in link or "k-vid.net" in link:
                item = GenericReportRow()
                item['licensor_name'] = licensor
                item['site_pagetitle'] = title
                item['site_link'] = response.url
                yield scrapy.Request(link, callback=self.parse_for_kvid, meta={'item': item})
            else:
                writer.write("./debug/dramanice.to/" + self.__timestamp,
                             "./debug/dramanice.to/" + self.__timestamp + "/links.txt",
                             licensor + "<<@>>" + title + "<<@>>" + response.url + "<<@>>" + "nil" + "<<@>>" + link)

    def parse_for_kvid(self, response):
        video_tag_links = response.xpath('//div[@class="videocontent"]//video//source/@src').extract()
        for link in video_tag_links:
            writer.write("./debug/dramanice.to/" + self.__timestamp,
                         "./debug/dramanice.to/" + self.__timestamp + "/links.txt",
                         response.meta['item']['licensor_name'] + "<<@>>" +
                         response.meta['item']['site_pagetitle'] + "<<@>>" +
                         response.meta['item']['site_link'] + "<<@>>" + response.url + "<<@>>" + link)
