from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from scrapy.exporters import JsonLinesItemExporter


class ItemPipeline(object):
    def __init__(self):
        self.ids_seen = set()
        self.file = None

    def open_spider(self, spider):
        self.file = open(spider.save_fname, 'wb')
        self.exporter = JsonLinesItemExporter(self.file)

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter['url'] in self.ids_seen:
            raise DropItem(f"Duplicate item found: {item!r}")
        else:
            self.ids_seen.add(adapter['url'])
            # from pdb import set_trace
            # set_trace()
            self.exporter.export_item(item)

            return item