import logging
from peewee import IntegrityError
from crawler.models import TableWlg

from crawler.spiders.spider_wlg import SpiderWlg


class PipelineWlg(object):
    def __init__(self):
        self.logger = logging.getLogger("PipelineWlg")

    def process_item(self, item, spider):
        if spider.name == SpiderWlg.name:
            try:
                TableWlg.create(**dict(item))
                self.logger.info("Got item. uid:{:s}".format(item['uid']))
            except IntegrityError:
                self.logger.warning("Item already exists. uid:{:s}".format(item['uid']))
        return item
