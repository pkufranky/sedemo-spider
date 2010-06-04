from scrapy.http import Request
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib_exp.crawlspider import CrawlSpider

class BaseCrawlSpider(CrawlSpider):
    priority_home = 10
    priority_list = 20
    priority_item = 30

    def extract_links(self, response, **extra): # {{{
        """ Extract links from response
        extra - passed to SgmlLinkExtractor
        """

        link_extractor = SgmlLinkExtractor(**extra)
        links = link_extractor.extract_links(response)

        return links
    # end def }}}
    def extract_requests(self, response, priority=0, **extra): # {{{
        links = self.extract_links(response, **extra)
        reqs = [self.make_request(link.url, priority=priority) for link in links]
        return reqs
    # end def }}}
    def make_request(self, url, **kw): # {{{
        kw.setdefault('callback', self.parse)
        return Request(url, **kw)
    # end def }}}
