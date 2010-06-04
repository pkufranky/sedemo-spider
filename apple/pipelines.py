from apple.contrib.store import StoreItem

class StoragePipeline(StoreItem):
    def process_item(self, spider, item): # {{{
        self.store_item(item, spider)
        return item
    # end def }}}

