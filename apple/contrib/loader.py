# -*- coding: utf-8 -*-

from scrapy.contrib.loader import XPathItemLoader, RegexItemLoader
from scrapy.contrib.loader.processor import TakeFirst, Compose, Strip, RemoveTag, Replace
from scrapy.utils.markup import remove_entities

html_processor = Compose(TakeFirst(), RemoveTag(keep=('br', 'p')), Replace(r'[\r\n]+|<br/?>', '<br />'), Strip())
text_processor = Compose(TakeFirst(), RemoveTag(), remove_entities, Strip())
class DefaultXPathItemLoader(XPathItemLoader):
    default_output_processor = text_processor
    intro_out = html_processor

