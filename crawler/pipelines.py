import logging
from peewee import IntegrityError
from crawler.models import TableWlg, TableJc56, TableBfb56, TableUfsoo

from crawler.spiders import SpiderWlg, SpiderJc56, SpiderJc56Full, SpiderBfb56, SpiderBfb56Full, SpiderUfsooFull


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


class PipelineJc56(object):
    def __init__(self):
        self.logger = logging.getLogger('PipelineJc56')

    def process_item(self, item, spider):
        if spider.name in [SpiderJc56.name, SpiderJc56Full.name]:
            try:
                TableJc56.create(**dict(item))
                self.logger.info("Got item. uid:{:d}".format(item['uid']))
            except IntegrityError:
                self.logger.warning("Item already exists. uid:{:d}".format(item['uid']))
        return item


class PipelineBfb56(object):
    def __init__(self):
        self.logger = logging.getLogger('PipelineBfb56')

    def process_item(self, item, spider):
        if spider.name in [SpiderBfb56.name, SpiderBfb56Full.name]:
            try:
                TableBfb56.create(**dict(item))
                self.logger.info("Got item. uid:{:s}".format(item['uid']))
            except IntegrityError:
                self.logger.warning("Item already exists. uid:{:s}".format(item['uid']))
        return item


class PipelineUfsoo(object):
    def __init__(self):
        self.logger = logging.getLogger('PipelineUfsoo')

    def process_item(self, item, spider):
        if spider.name in [SpiderUfsooFull.name]:
            try:
                TableUfsoo.create(**dict(item))
                self.logger.info("Got item. uid:{:s}".format(item['uid']))
            except IntegrityError:
                self.logger.warning("Item already exists. uid:{:s}".format(item['uid']))
        return item
