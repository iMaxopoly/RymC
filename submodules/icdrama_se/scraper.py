import json

import execjs
import scrapy
import scrapy_splash
from scrapy_splash import SplashRequest

import writer
from find_licensor import find_licensor
from report_structure import GenericReportRow
from string_utils import find_between

if __name__ == "__main__":
    print("file is meant for import.")
    exit()


class IcdramaSe(scrapy.Spider):
    __domain = "icdrama.se"
    __protocol = "http"
    __baseURL = __protocol + "://" + __domain
    __timestamp = ""
    __clients = None
    __js_funcs = execjs.compile(
        """function strreverse(a){return a.split("").reverse().join("")} function atob(a){var b,c,d,e,f,g,
        h;for(g=a.length,f=0,h="";f<g;){do b=base64DecodeChars[255&a.charCodeAt(f++)];while(f<g&&b==-1);if(b==-1)break;do
        c=base64DecodeChars[255&a.charCodeAt(f++)];while(f<g&&c==-1);if(c==-1)break;h+=String.fromCharCode(b<<2|(
        48&c)>>4);do{if(d=255&a.charCodeAt(f++),61==d)return h;d=base64DecodeChars[d]}while(f<g&&d==-1);if(
        d==-1)break;h+=String.fromCharCode((15&c)<<4|(60&d)>>2);do{if(e=255&a.charCodeAt(f++),61==e)return
        h;e=base64DecodeChars[e]}while(f<g&&e==-1);if(e==-1)break;h+=String.fromCharCode((3&d)<<6|e)}return h}var
        base64DecodeChars=new Array(-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,
        -1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,62,-1,-1,-1,63,52,53,54,55,56,57,58,59,60,61,-1,-1,-1,-1,-1,-1,-1,0,
        1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,-1,-1,-1,-1,-1,-1,26,27,28,29,30,31,32,33,34,
        35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,-1,-1,-1,-1,-1); """
    )

    name = __domain
    allowed_domains = [__domain, "videobug.se"]
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

    custom_settings = {"SPLASH_URL": 'http://192.168.99.100:8050',
                       "DOWNLOADER_MIDDLEWARES": {
                           'scrapy_splash.SplashCookiesMiddleware': 723,
                           'scrapy_splash.SplashMiddleware': 725,
                           'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810
                       },
                       "SPIDER_MIDDLEWARES": {'scrapy_splash.SplashDeduplicateArgsMiddleware': 100},
                       "DUPEFILTER_CLASS": 'scrapy_splash.SplashAwareDupeFilter',
                       "HTTPCACHE_STORAGE": 'scrapy_splash.SplashAwareFSCacheStorage'}

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
        item = GenericReportRow()
        item['licensor_name'] = licensor
        item['site_pagetitle'] = title
        item['site_link'] = response.url
        for link in links:
            yield SplashRequest(link, self.parse_for_videobug, args={'wait': 0.5},
                                slot_policy=scrapy_splash.SlotPolicy.SINGLE_SLOT,
                                meta={'item': item})

    def parse_for_videobug(self, response):
        json_body = find_between(response.body, "var	json_data = '", "';").strip()
        if len(json_body) < 1:
            return
        try:
            j_objects = json.loads(json_body)
            for link_hash in j_objects:
                link_hash_stripped = link_hash["u"].strip()
                if len(link_hash_stripped) < 1:
                    continue
                deciphered_link = self.decrypt_videobug_url(link_hash_stripped)
                if deciphered_link == "":
                    continue
                writer.write("./debug/icdrama.se/" + self.__timestamp,
                             "./debug/icdrama.se/" + self.__timestamp + "/links.txt",
                             response.meta['item']['licensor_name'] + "<<@>>" +
                             response.meta['item']['site_pagetitle'] + "<<@>>" +
                             response.meta['item']['site_link'] + "<<@>>" + response.url + "<<@>>" + deciphered_link)
        except ValueError:
            return

    def decrypt_videobug_url(self, encrypted_url):
        try:
            decrypted = self.__js_funcs.call("atob", execjs.eval('"' + encrypted_url + '"'))
        except RuntimeError:
            return ""
        if decrypted is None:
            return ""
        decrypted = decrypted.strip()
        if len(decrypted) < 1:
            return ""
        return decrypted
