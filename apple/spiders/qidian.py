# -*- coding: utf-8 -*-

import re
from scrapy.contrib_exp.crawlspider import Rule
from scrapy.contrib.loader.processor import TakeFirst, RemoveTag

from apple.contrib.spider import BaseCrawlSpider
from apple.items import NovelItem
from apple.contrib.loader import DefaultXPathItemLoader

class QidianSpider(BaseCrawlSpider):
    name = 'qidian'
    allowed_domains = ["qidian.com"]
    regex_home = r'http://all.qidian.com/$'
    regex_list = r'bookstore.aspx\?.*ChannelId=-1&.*PageIndex=\d+'
    regex_item = r'Book/\d+\.aspx$'
    start_urls = [
            'http://all.qidian.com/',
            ]

    rules = [
            Rule(regex_home, 'parse_home'),
            Rule(regex_list, 'parse_list'),
            Rule(regex_item, 'parse_item'),
            ]

    def parse_home(self, response): # {{{
        links = self.extract_links(response, allow=self.regex_list, restrict_xpaths='.storelistbottom')

        m = re.search(ur'GoPage.*1/(\d+).*?页', response.body_as_unicode(), re.M)
        total_page = int(m.group(1))

        reqs = []
        for p in range(1, total_page+1):
            url = re.sub('PageIndex=\d+', 'PageIndex=%d' % p, links[0].url)
            req = self.make_request(url, priority=self.priority_list)
            reqs.append(req)
        return reqs
    # end def }}}

    def parse_list(self, response): # {{{
        reqs = self.extract_requests(response, priority=self.priority_item, allow=self.regex_item)
        return reqs
    # end def }}}

    def parse_item(self, response): # {{{
        loader = DefaultXPathItemLoader(NovelItem(), response=response)
        loader.add_xpath('name', 'div.book_info div.title h1')
        loader.add_xpath('intro', 'div.book_info div.intro div.txt', TakeFirst(), RemoveTag('div'))
        loader.add_xpath('img_url', 'div.book_pic img/@src')
        loader.add_value('page_url', response.url)

        item = loader.load_item()

        return item
    # end def }}}

SPIDER = QidianSpider()
