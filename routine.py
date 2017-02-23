from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from twisted.internet import defer
from twisted.internet import reactor

from report_0_hop import prepare_0_hop_report
from report_1_hop import prepare_1_hop_report
from submodules.dopeka_com.scraper import DopekaCom
from submodules.doramasjc_com.scraper import DoramasjcCom
from submodules.doramastv_com.scraper import DoramastvCom
from submodules.dramago_com.scraper import DramagoCom
from submodules.dramalove_tv.scraper import DramaloveTv
from submodules.dramanice_to.scraper import DramaniceTo
from submodules.estrenosdoramas_net.scraper import EstrenosdoramasNet
from submodules.gooddrama_to.scraper import GooddramaTo
from submodules.icdrama_se.scraper import IcdramaSe
from submodules.myasiantv_se.scraper import MyasiantvSe
from submodules.nineanime_to.scraper import NineanimeTo
from submodules.novelascoreanas_es.scraper import NovelascoreanasEs


def routine(timestamp, args, clients):
    print timestamp, args

    configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
    runner = CrawlerRunner({
        "CONCURRENT_REQUESTS": 300,
        "CONCURRENT_REQUESTS_PER_DOMAIN": args.workers,
        "USER_AGENT": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 "
                      "Safari/537.36"
    })

    if args.subparser_name == "boxasian.com" \
            or args.subparser_name == "kissasian.com":
        print "Not implemented yet."
        return

    @defer.inlineCallbacks
    def crawl():
        if args.subparser_name == "icdrama.se":
            yield runner.crawl(IcdramaSe, time_stamp=timestamp, clients=clients)
        elif args.subparser_name == "novelascoreanas.es":
            yield runner.crawl(NovelascoreanasEs, time_stamp=timestamp, clients=clients)
        elif args.subparser_name == "estrenosdoramas.net":
            yield runner.crawl(EstrenosdoramasNet, time_stamp=timestamp, clients=clients)
        elif args.subparser_name == "dopeka.com":
            yield runner.crawl(DopekaCom, time_stamp=timestamp, clients=clients)
        elif args.subparser_name == "myasiantv.se":
            yield runner.crawl(MyasiantvSe, time_stamp=timestamp, clients=clients)
        elif args.subparser_name == "doramasjc.com":
            yield runner.crawl(DoramasjcCom, time_stamp=timestamp, clients=clients)
        elif args.subparser_name == "boxasian.com":
            yield runner.crawl(IcdramaSe, time_stamp=timestamp, clients=clients)
        elif args.subparser_name == "gooddrama.to":
            yield runner.crawl(GooddramaTo, time_stamp=timestamp, clients=clients)
        elif args.subparser_name == "dramago.com":
            yield runner.crawl(DramagoCom, time_stamp=timestamp, clients=clients)
        elif args.subparser_name == "dramalove.tv":
            yield runner.crawl(DramaloveTv, time_stamp=timestamp, clients=clients)
        elif args.subparser_name == "doramastv.com":
            yield runner.crawl(DoramastvCom, time_stamp=timestamp, clients=clients)
        elif args.subparser_name == "dramanice.to":
            yield runner.crawl(DramaniceTo, time_stamp=timestamp, clients=clients)
        elif args.subparser_name == "9anime.to":
            yield runner.crawl(NineanimeTo, time_stamp=timestamp, clients=clients)
        reactor.stop()

    crawl()
    reactor.run()

    if args.subparser_name == "estrenosdoramas.net":
        prepare_0_hop_report(args.savepath, "estrenosdoramas.net", timestamp)
    elif args.subparser_name == "novelascoreanas.es":
        prepare_0_hop_report(args.savepath, "novelascoreanas.es", timestamp)
    elif args.subparser_name == "dopeka.com":
        prepare_0_hop_report(args.savepath, "dopeka.com", timestamp)
    elif args.subparser_name == "myasiantv.se":
        prepare_0_hop_report(args.savepath, "myasiantv.se", timestamp)
    elif args.subparser_name == "doramasjc.com":
        prepare_0_hop_report(args.savepath, "doramasjc.com", timestamp)
    elif args.subparser_name == "9anime.to":
        prepare_0_hop_report(args.savepath, "9anime.to", timestamp)
    elif args.subparser_name == "gooddrama.to":
        prepare_1_hop_report(args.savepath, "gooddrama.to", timestamp)
    elif args.subparser_name == "dramago.com":
        prepare_1_hop_report(args.savepath, "dramago.com", timestamp)
    elif args.subparser_name == "dramalove.tv":
        prepare_1_hop_report(args.savepath, "dramalove.tv", timestamp)
    elif args.subparser_name == "dramanice.to":
        prepare_1_hop_report(args.savepath, "dramanice.to", timestamp)
    elif args.subparser_name == "doramastv.com":
        prepare_1_hop_report(args.savepath, "doramastv.com", timestamp)
    elif args.subparser_name == "icdrama.se":
        prepare_1_hop_report(args.savepath, "icdrama.se", timestamp)
    # elif args.subparser_name == "icdrama.se":
    #     iframe_objs = read("./debug/icdrama.se/" + timestamp + "/links.txt")
    #
    #     pool = Pool(processes=args.chromeWorkers)
    #     for i in pool.imap_unordered(videobug, iframe_objs):
    #         if len(i) <= 0:
    #             continue
    #         for l in i:
    #             write("./debug/icdrama.se/" + timestamp, "./debug/icdrama.se/" + timestamp + "/cyberlocker-links.txt",
    #                   l)
    #
    #     pool.close()
    #     pool.join()
    #
    #     from submodules.icdrama_se.custom_report import prepare_report
    #     prepare_report(args.savepath, timestamp)
