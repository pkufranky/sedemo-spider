# -*- coding: utf-8 -*-

import re
from apple.spiders.qidian import QidianSpider
from apple.tests.spider_test import SpiderTestCase

class QidianSpiderTestCase(SpiderTestCase): # {{{
    def setUp(self):
        self.spider = QidianSpider()

    def test_parse_home(self): # {{{
        url = 'http://all.qidian.com/'
        reqs = self._parse(url)
        self.assertGreater(len(reqs), 2000, url)
        self.assertReMatch('http://.+bookstore\.aspx\?.*ChannelId=-1.*PageIndex=2', reqs[1].url, url)
    # end def }}}

    def test_parse_list(self): # {{{
        url = 'http://www.qidian.com/book/bookstore.aspx?ChannelId=-1&SubCategoryId=-1&Tag=all&Size=-1&Action=-1&OrderId=6&P=all&PageIndex=1&update=-1&Vip=-1'
        reqs = self._parse(url)
        self.assertEqual(len(reqs), 100, url)
        self.assertReMatch(self.spider.regex_item, reqs[1].url, url)
    # end def }}}

    def test_parse_item(self): # {{{
        def test(url, expected):
            item = self._parse_one(url)
            self.assertObjectMatch(expected, item, url)

        url = 'http://www.qidian.com/Book/172.aspx'
        expected = {
                'name': u'女人街的除魔事务所',
                'r:intro': u'<br />.*让我深刻体味这可怕的魔鬼吧',
                'img_url': u'http://image.cmfu.com/books/1.jpg',
                'page_url': url,
                }
        test(url, expected)
    # end def }}}

# end class }}}
