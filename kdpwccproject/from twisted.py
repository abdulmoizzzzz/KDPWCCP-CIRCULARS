from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging
from kdpwccproject.spiders.kdpwcc_spider import KdpwccSpider
from kdpwccproject.spiders.kdpwcc_spider2 import KdpwccSpider

configure_logging()
settings = get_project_settings()
runner = CrawlerRunner(settings)

runner.crawl(KdpwccSpider)
runner.crawl(KdpwccSpider)

d = runner.join()
d.addBoth(lambda _: reactor.stop())

reactor.run()  
