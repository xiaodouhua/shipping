import scrapy
import re
from crawler.items import ItemBfb56


class SpiderBfb56Full(scrapy.Spider):
    name = 'bfb56_full'

    auto_paginate = True

    def start_requests(self):
        yield scrapy.Request(
            'http://www.bfb56.com/freights/fcl-1.html',
            headers={'Referer': 'http://www.bfb56.com/freights/fcl-2.html'},
        )

    def parse(self, response):
        if self.auto_paginate:
            next_page = response.xpath('//div[@class="pagination"]/a[@class="next_page"]/@href').extract_first()
            if next_page:
                yield scrapy.Request("http://www.bfb56.com" + next_page,
                                     headers={'Referer': response.url},
                                     callback=self.parse)

        for url in response.xpath('//dt[@class="transport-tit"]/a/@href').extract():
            yield scrapy.Request(url, headers={'Referer': response.url}, callback=self.parse_item)

    def parse_item(self, response):
        uid = re.search('item\-(.*?)\.html', response.url)
        if uid:
            uid = uid.group(1)
        else:
            yield None
            raise StopIteration()

        prices = response.xpath('//table[@class="contrPrice"]/tr/td/span/text()').extract()
        price_20gp, price_40gp, price_40hq = None, None, None
        try:
            price_20gp = int(prices[0].strip())
            price_40gp = int(prices[1].strip())
            price_40hq = int(prices[2].strip())
        except (ValueError, TypeError, IndexError):
            pass

        starting_port, starting_port_en, destination_port, destination_port_en = None, None, None, None
        ports = response.xpath('//div[@class="contrCard"]/h2/text()').extract_first()
        try:
            starting_port = ports.split("—")[0].split(")")[0].split("(")[0]
            starting_port_en = ports.split("—")[0].split(")")[0].split("(")[1].strip()
            destination_port = ports.split("—")[1].split(")")[0].split("(")[0].strip()
            destination_port_en = ports.split("—")[1].split(")")[0].split("(")[1].strip()
        except (IndexError, TypeError):
            pass

        valid_date = response.xpath('//div[@class="contrCard"]/p[@class="auth-deadline"]/text()').extract_first()
        valid_date = valid_date.split("：") if valid_date else []
        valid_date = valid_date[1].strip() if len(valid_date) > 0 else None

        duration, company, schedule, cargo_type = -1, None, None, None
        for sel in response.xpath('//div[@class="f-item"]'):
            label = sel.xpath('label/text()').extract_first()
            data = sel.xpath('span/text()').extract_first()

            if '承 运 人' in label:
                company = data
            elif '离港班期' in label:
                schedule = data
            elif '航    程' in label:
                try:
                    duration = int(data)
                except (TypeError, ValueError):
                    pass
            elif '适用品名' in label:
                cargo_type = data

        yield ItemBfb56(
            uid=uid, starting_port=starting_port, starting_port_en=starting_port_en,
            destination_port=destination_port, destination_port_en=destination_port_en,
            company=company, valid_date=valid_date, duration=duration,
            schedule=schedule, cargo_type=cargo_type,
            price_20gp=price_20gp, price_40gp=price_40gp, price_40hq=price_40hq,
            url=response.url
        )


class SpiderBfb56(SpiderBfb56Full):
    name = 'bfb56'

    auto_paginate = False

    def start_requests(self):
        for i in range(1, 11):
            yield scrapy.Request(
                'http://www.bfb56.com/freights/fcl-{:d}.html'.format(i),
                headers={'Referer': 'http://www.bfb56.com/freights/fcl-{:d}.html'.format(i if i > 1 else 2)},
                callback=self.parse)
