import simplejson as json

from scrapy import log
from scrapy.conf import settings
from scrapy.core.exceptions import NotConfigured

from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.sql import select
from sqlalchemy.sql.expression import func

class StoreItem(object):

    def __init__(self): # {{{
        db_url = settings.get("DB_URL")
        table_name = settings.get("DB_TABLE")
        if not db_url or not table_name:
            raise NotConfigured
        self.engine = create_engine(db_url, echo=False)
        self.metadata = MetaData(bind=self.engine)
        self.table = Table(table_name, self.metadata, autoload=True)
    # end def }}}

    def store_item(self, item, spider): # {{{
        item_table = self.table

        dbobj = {}
        for k,v in item.iteritems():
            if isinstance(v, list) or isinstance(v, dict):
                dbobj[k] = json.dumps(v)
            else:
                dbobj[k] = v

        conn = self.engine.connect()

        page_url = item['page_url']
        where = item_table.c.page_url == page_url
        sel = select([func.count(item_table.c.id)]).where(where)
        cnt = conn.execute(sel).scalar()
        if cnt:
            assert cnt==1, 'More than one item with page_url %s' % page_url
            upd = item_table.update().where(where)
            conn.execute(upd, dbobj)
            status = 'updated'
        else:
            ins = item_table.insert()
            conn.execute(ins, dbobj)
            status = 'inserted'
        log.msg('Item %s into %s: %s' % (status, item_table.name, page_url), level=log.DEBUG, spider=spider)

        conn.close()
    # end def }}}
