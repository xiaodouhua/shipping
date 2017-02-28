import re
from scrapy.exceptions import IgnoreRequest

from crawler.models import TableUfsoo


class UfsooDownloadMiddleware(object):
    def process_request(self, request, spider):
        uid = re.search('http://www.ufsoo.com/fcl/(.*?)-\d+-\d+.html', request.url)
        if uid:
            uid = uid.group(1)
            if TableUfsoo.select().where(TableUfsoo.uid == uid).exists():
                raise IgnoreRequest()
