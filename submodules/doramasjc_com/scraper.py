import json

import scrapy

import writer
from find_licensor import find_licensor
from report_structure import GenericReportRow
from string_utils import find_between

if __name__ == "__main__":
    print("file is meant for import.")
    exit()


class DoramasjcCom(scrapy.Spider):
    __domain = "www.doramasjc.com"
    __protocol = "http"
    __baseURL = __protocol + "://" + __domain
    __timestamp = ""
    __clients = None

    name = __domain
    allowed_domains = [__domain, "amazonaws.com"]
    start_urls = [
        __baseURL + "/doramas/"
    ]
    handle_httpstatus_list = [410]

    def __init__(self, time_stamp, clients, **kwargs):
        self.__timestamp = time_stamp
        self.__clients = clients
        super(DoramasjcCom, self).__init__(**kwargs)

    def parse(self, response):
        links = response.xpath("//div[@class='aboxy_lista']/a/@href").extract()
        next_page_text = response.xpath("//div[@class='pagin']/span/a[last()]/text()").extract_first()
        if "Siguiente" in next_page_text:
            next_page_link = response.xpath("//div[@class='pagin']/span/a[last()]/@href").extract_first()
            yield scrapy.Request(response.urljoin("/doramas/" + next_page_link), callback=self.parse)
        for link in links:
            yield scrapy.Request(link, callback=self.parse_for_episodes)

    def parse_for_episodes(self, response):
        links = response.xpath(
            "//ul[@id='listado_epis']/li/a/@href"
        ).extract()
        for link in links:
            yield scrapy.Request(link, callback=self.parse_for_iframes)

    def parse_for_iframes(self, response):
        title = response.xpath('/html/head/title/text()').extract_first()
        links = response.xpath('//div[@class="tab_content"]/iframe/@src').extract()
        licensor = find_licensor(title, self.__clients)
        item = GenericReportRow()
        item['licensor_name'] = licensor
        item['site_pagetitle'] = title
        item['site_link'] = response.url
        for link in links:
            if link.startswith("//"):
                link = "http:" + link
            if "www.doramasjc.com/gkphp" in link:
                yield scrapy.Request(link, callback=self.parse_for_gkphp, meta={'item': item})
            else:
                writer.write("./debug/doramasjc.com/" + self.__timestamp,
                             "./debug/doramasjc.com/" + self.__timestamp + "/links.txt",
                             licensor + "<<@>>" + title + "<<@>>" + response.url + "<<@>>" + link)

    def parse_for_gkphp(self, response):
        html = response.body
        if "ucloud.php" in response.url:
            link = find_between(html, 'file:"', '",')
            writer.write("./debug/doramasjc.com/" + self.__timestamp,
                         "./debug/doramasjc.com/" + self.__timestamp + "/links.txt",
                         response.meta['item']['licensor_name'] + "<<@>>" +
                         response.meta['item']['site_pagetitle'] + "<<@>>" +
                         response.meta['item']['site_link'] + "<<@>>" + link)
        elif "oklass.php" in response.url:
            pass
        elif "api.doramasjc.com" in response.url:
            count = 0
            while True:
                if count > 10:
                    break
                result = find_between(html, '{file: "', '"')
                if result is "":
                    break
                writer.write("./debug/doramasjc.com/" + self.__timestamp,
                             "./debug/doramasjc.com/" + self.__timestamp + "/links.txt",
                             response.meta['item']['licensor_name'] + "<<@>>" +
                             response.meta['item']['site_pagetitle'] + "<<@>>" +
                             response.meta['item']['site_link'] + "<<@>>" + result)
                index = html.index('{file: "')
                html = html[index + len('{file: "'):]
                count += 1
        elif "html5.php" in response.url:
            source = response.xpath('//video[@id="myvideo"]/source/@src').extract_first()
            yield scrapy.Request(source, callback=self.parse_for_html5, meta={'item': response.meta['item']})

        elif "hulu.php" in response.url:
            key = find_between(response.body, '{link:"', '"').strip(' \t\n\r')
            yield scrapy.FormRequest('http://www.doramasjc.com/gkphp/plugins/gkpluginsphp.php',
                                     formdata={'link': key},
                                     callback=self.parse_for_hulu, meta={'item': response.meta['item']})

    def parse_for_hulu(self, response):
        try:
            obj = json.loads(response.body)
        except ValueError:
            return
        writer.write("./debug/doramasjc.com/" + self.__timestamp,
                     "./debug/doramasjc.com/" + self.__timestamp + "/links.txt",
                     response.meta['item']['licensor_name'] + "<<@>>" +
                     response.meta['item']['site_pagetitle'] + "<<@>>" +
                     response.meta['item']['site_link'] + "<<@>>" + obj['link'])

    def parse_for_html5(self, response):
        writer.write("./debug/doramasjc.com/" + self.__timestamp,
                     "./debug/doramasjc.com/" + self.__timestamp + "/links.txt",
                     response.meta['item']['licensor_name'] + "<<@>>" +
                     response.meta['item']['site_pagetitle'] + "<<@>>" +
                     response.meta['item']['site_link'] + "<<@>>" + response.url)
