# -*- coding: utf-8 -*-
import re
from urllib2 import urlopen
from twisted.trial import unittest
from scrapy.utils.python import unicode_to_str
from scrapy.http import HtmlResponse
from scrapy.http import Request
from scrapy.utils.misc import arg_to_iter

class SpiderTestCase(unittest.TestCase): # {{{
    def setUp(self):
        self.spider = None
    def tearDown(self):
        pass

    def _get_page(self, url=None, data=None, req=None): # {{{
        """ Get response from url or request

        if req is given, url/data is not used
        if data is given, issue POST
        """

        if not req:
            req = Request(url, method='POST', body=data) if data else Request(url)

        r = urlopen(req.url, req.body) if req.method == 'POST' else urlopen(req.url)

        contentType = r.info().getheader('Content-Type', None)
        headers = {}
        if contentType:
            headers['Content-Type'] = contentType

        response = HtmlResponse(req.url, body=r.read(), headers=headers)
        response.request = req
        return response
    # end def }}}

    def _parse(self, url=None, data=None, req=None):
        r = self._get_page(url=url, data=data, req=req)
        return list(self.spider.parse(r))

    def _parse_one(self, url=None, data=None, req=None):
        results = self._parse(url=url, data=data, req=req)
        assert len(results) == 1
        return results[0]

    def assertObjectsMatch(self, expected, actuals, msg=None, keys = None): # {{{
        for actual in actuals:
            self.assertObjectMatch(expected, actual, msg, keys)
    # end def }}}

    def assertObjectMatch(self, expected, actual, msg=None, keys = None): # {{{
        """If key starts with r:, do regex match, else do equal test"""
        actual_is_dict = hasattr(actual, '__getitem__')
        def my_type(o):
            return str(type(o))[7:-2]

        def parse_key(key):
            how = None
            parts = key.split(':')
            if len(parts) == 2:
                how, key = parts[0], parts[1]
            return (how, key)

        def get_value(obj, key):
            if actual_is_dict:
                return obj.get(key, None)
            else:
                return getattr(obj, key, None)

        def check_match(expected, actual, how):
            if how == 'r': # regex match
                if not expected or not actual:
                    return expected == actual
                else:
                    return re.search(expected, actual) != None
            else:
                return expected == actual

        keys = keys or expected.keys()
        err_lines = []
        for key in keys:
            how, actual_key = parse_key(key)
            ev = expected[key]
            av = get_value(actual, actual_key)
            if not check_match(ev, av, how):
                errmsg = '%s: %s %s != %s %s' % (key, my_type(ev), ev, my_type(av), av)
                err_lines.append(errmsg)
        # end for

        errmsg = '\n'.join(err_lines)
        if msg:
            errmsg = msg + '\n' + errmsg
        self.failIf(err_lines, unicode_to_str(errmsg))
    # end def }}}

    def assertReMatch(self, regex, actual, msg=None) : # {{{
        actuals = arg_to_iter(actual)
        for actual in actuals:
            match = re.search(regex, actual)
            errmsg = "%s not match %s" % (actual, regex)
            if msg:
                errmsg = '%s\n%s' % (msg, errmsg)
            self.assertTrue(match, errmsg)
    # end def }}}

    def assertGreater(self, first, second, msg=None):
        self.assertCompare(first, second, '>', msg)
    def assertLess(self, first, second, msg=None):
        self.assertCompare(first, second, '<', msg)
    def assertCompare(self, first, second, op='==', msg=None): # {{{
        errmsg = "%d %s %d" % (first, op, second)
        if msg:
            errmsg = '%s\n%s' % (msg, errmsg)
        if op == '==':
            r = first == second
        elif op == '!=':
            r = first != second
        elif op == '>':
            r = first > second
        elif op == '<':
            r = first < second
        elif op == '<=':
            r = first <= second
        elif op == '>=':
            r = first >= second
        else:
            self.fail('Bad op %s' % op)

        self.assertTrue(r, errmsg)
    # end def }}}

# end class }}}
