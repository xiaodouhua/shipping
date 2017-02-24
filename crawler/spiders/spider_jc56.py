import scrapy
from crawler.items import ItemJc56
from crawler.models import TableJc56


def safe_to_int(string):
    try:
        return int(string.strip()) if string else None
    except (ValueError, TypeError):
        return None


def safe_split_extract(string, sep, index):
    lst = string.split(sep) if string else []
    try:
        data = lst[index].strip()
        return data if len(data) != 0 else None
    except IndexError:
        return None


class SpiderJc56(scrapy.Spider):
    """
    http://jc56.com/ uid 从0开始依次递增
    """
    name = "jc56"

    def start_requests(self):
        yield self.make_index_request()

    def parse(self, response):
        page = response.meta['page']

        for uid in response.xpath('//div[@class="hyyj"]').re('/feight/GPDetail/(\d+).html'):
            try:
                uid = int(uid.strip())
            except Exception:
                continue
            yield self.make_detail_request(uid, 'http://jc56.com/feight/GPList/-------{:d}.html'.format(page))

        page_count = response.xpath('//div[@id="page_abc"]').re_first('<span class="page_sum">共(\d+)页</span>')
        if page == 1:
            for i in range(2, int(page_count) + 1):
                yield self.make_index_request(i)

    def parse_item(self, response):
        uid = response.meta['uid']

        starting_port = response.xpath('//div[@id="price_detail"]/ul[1]/li[1]/text()').extract_first()
        starting_port = safe_split_extract(starting_port, '：', -1)

        destination_port = response.xpath('//div[@id="price_detail"]/ul[1]/li[2]/text()').extract_first()
        destination_port = safe_split_extract(destination_port, '：', -1)

        transit_port = response.xpath('//div[@id="price_detail"]/ul[2]/li[2]/text()').extract_first()
        transit_port = safe_split_extract(transit_port, '：', -1)

        route = response.xpath('//div[@id="price_detail"]/ul[1]/li[3]/text()').extract_first()
        route = safe_split_extract(route, '：', -1)

        company = response.xpath('//div[@id="price_detail"]/ul[1]/li[4]/text()').extract_first()
        company = safe_split_extract(company, '：', -1)

        duration = response.xpath('//div[@id="price_detail"]/ul[2]/li[3]/text()').extract_first()
        duration = safe_split_extract(duration, '：', -1)
        duration = safe_to_int(duration)

        schedule = response.xpath('//div[@id="price_detail"]/ul[3]/li[1]/b/text()').extract_first()
        schedule = safe_split_extract(schedule, '：', -1)

        valid_from_date = response.xpath('//div[@id="price_detail"]/ul[3]/li[2]/text()').extract_first()
        valid_from_date = safe_split_extract(valid_from_date, '\r\n', -4)

        valid_to_date = response.xpath('//div[@id="price_detail"]/ul[3]/li[2]/text()').extract_first()
        valid_to_date = safe_split_extract(valid_to_date, '\r\n', -2)

        price_20gp = response.xpath('//*[@id="menuk_1"]/b/text()').extract_first()
        price_20gp = safe_to_int(price_20gp)

        price_40gp = response.xpath('//*[@id="menuk_2"]/b/text()').extract_first()
        price_40gp = safe_to_int(price_40gp)

        price_40hq = response.xpath('//*[@id="menuk_2"]/b/text()').extract_first()
        price_40hq = safe_to_int(price_40hq)

        surcharge = response.xpath('//div[@id="price_detail"]/ul[2]/li[4]/text()').extract_first()
        surcharge = safe_split_extract(surcharge, '：', -1)

        remarks = response.xpath('//div[@id="price_detail"]/ul[4]/li/text()').extract_first()
        remarks = safe_split_extract(remarks, '：', -1)

        yield ItemJc56(
            uid=uid, starting_port=starting_port, destination_port=destination_port,
            transit_port=transit_port, route=route, company=company,
            duration=duration, schedule=schedule,
            valid_from_date=valid_from_date, valid_to_date=valid_to_date,
            price_20gp=price_20gp, price_40gp=price_40gp, price_40hq=price_40hq,
            surcharge=surcharge, remarks=remarks
        )

        # for _uid in response.xpath('//div[@class="detail_con"]').re('/feight/GPDetail/(\d+).html'):
        #     yield self.make_detail_request(_uid, response.url)

    def make_index_request(self, page=1):
        url = 'http://jc56.com/feight/GPList/-------{:d}.html'.format(page)
        headers = {
            'Referer': 'http://jc56.com/feight/GPList/-------{:d}.html'.format(page - 1 if page > 1 else 2)
        }
        return scrapy.Request(url, headers=headers, meta={'page': page})

    def make_detail_request(self, uid, referer):
        return scrapy.Request(
            'http://jc56.com/feight/GPDetail/{:d}.html'.format(uid),
            headers={'Referer': referer},
            meta={'uid': uid},
            callback=self.parse_item
        )


class SpiderJc56Full(SpiderJc56):
    name = 'jc56_full'

    def start_requests(self):
        scraped = []
        for entry in TableJc56.select():
            scraped.append(entry.uid)

        for i in set(range(1, 57104)) - set(scraped):
            yield self.make_detail_request(i, 'http://jc56.com/')
