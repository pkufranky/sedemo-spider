# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class NovelItem(Item):
    name = Field()
    intro = Field()
    img_url = Field()
    page_url = Field()
