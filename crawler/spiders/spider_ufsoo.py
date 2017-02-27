import scrapy
import re
from crawler.items import ItemUfsoo


def safe_strip(string):
    return string.strip() if string else None


def safe_to_int(string):
    try:
        return int(string.strip()) if string else None
    except (ValueError, TypeError):
        return None


class SpiderUfsooFull(scrapy.Spider):
    name = "ufsoo_full"

    def start_requests(self):
        # 访问查询首页，用来获取航线链接，然后根据航线进行爬取
        yield scrapy.Request(
            'http://www.ufsoo.com/fcl',
            headers={'Referer': 'http://www.ufsoo.com/'},
            callback=self.parse_route
        )

    def parse_route(self, response):
        # 获取所有航线第一页
        for url in response.xpath(
                '//ul[preceding-sibling::h4[contains(text(),"航线")]]//a[@title]/@href').extract():
            yield scrapy.Request('http://www.ufsoo.com' + url.strip(), headers={'Referer': 'http://www.ufsoo.com/fcl/'},
                                 callback=self.parse_index)

    def parse_index(self, response):
        # 翻页
        next_page = response.xpath('//a[@title="下一页"]/@onclick').extract_first()
        if next_page:
            url = re.search("GoToPage\('(.*?\.html)'\)", next_page)
            if url:
                yield scrapy.Request(
                    'http://www.ufsoo.com' + url.group(1).strip(),
                    headers={'Referer': response.url},
                    callback=self.parse_index
                )

        # 报价详情
        for url in response.xpath('//table[@id="tableprice"]/tr/td/h3/a/@href').extract():
            yield scrapy.Request(
                'http://www.ufsoo.com' + url.strip(),
                headers={'Referer': response.url},
                callback=self.parse_item
            )

        # 历史报价第一页 (全是重复的)
        # for url in response.xpath('//a[child::input[@class="checkhistorybtn"]]/@href').extract():
        #     yield scrapy.Request(
        #         'http://www.ufsoo.com' + url.strip(),
        #         headers={'Referer': response.url},
        #         callback=self.parse_index
        #     )

    def parse_item(self, response):

        uid = re.search('http://www.ufsoo.com/fcl/(.*?)-\d+-\d+.html', response.url)
        if uid:
            uid = uid.group(1)
        else:
            yield None
            raise StopIteration()

        left_info = response.xpath('//div[contains(@class,"flight_info") and '
                                   'following-sibling::div[contains(@class,"flight_arrow")]]')

        right_info = response.xpath('//div[contains(@class,"flight_info") and '
                                    'preceding-sibling::div[contains(@class,"flight_arrow")]]')

        starting_port_info = left_info.xpath('//a[preceding-sibling::label[text()="起运港"]]')
        starting_port = starting_port_info.xpath('@title').extract_first()
        starting_port_en = starting_port_info.xpath('em/text()').extract_first()

        valid_from_date = left_info.xpath('//li[child::label[text()="生效时间"]]/text()').extract_first()
        valid_to_date = right_info.xpath('//em[preceding-sibling::label[text()="截止时间"]]/text()').extract_first()

        route = left_info.xpath('//li[child::label[text()="航线"]]/text()').extract_first()

        currency_unit = right_info.xpath('//li[child::label[text()="货币单位"]]/text()').extract_first()

        destination_info = right_info.xpath('//a[preceding-sibling::label[text()="目的港"]]')
        destination_port = destination_info.xpath('@title').extract_first()
        destination_port_en = destination_info.xpath('text()').extract_first()

        company_info = right_info.xpath('//a[preceding-sibling::label[text()="船公司"]]')
        company = company_info.xpath('@title').extract_first()
        company_en = company_info.xpath('text()').extract_first()

        transit_port_info = left_info.xpath('//a[preceding-sibling::label[text()="中转港"]]')
        transit_port = transit_port_info.xpath('@title').extract_first()
        transit_port_en = transit_port_info.xpath('text()').extract_first()

        duration = right_info.xpath('//li[child::label[text()="航程"]]/text()').extract_first()
        date_set_sail = right_info.xpath('//a[preceding-sibling::label[text()="出发日"]]/text()').extract_first()
        date_cut_off = left_info.xpath('//a[preceding-sibling::label[text()="截关日"]]/text()').extract_first()

        prices = response.xpath('//ul[@class="detail_prices"]')
        price_20gp = prices.xpath('//div[following-sibling::p[text()="20GP"]]/em/text()').extract_first()
        price_40gp = prices.xpath('//div[following-sibling::p[text()="40GP"]]/em/text()').extract_first()
        price_40hq = prices.xpath('//div[following-sibling::p[text()="40HQ"]]/em/text()').extract_first()

        yield ItemUfsoo(
            uid=uid, starting_port=safe_strip(starting_port), starting_port_en=safe_strip(starting_port_en),
            destination_port=safe_strip(destination_port), destination_port_en=safe_strip(destination_port_en),
            transit_port=safe_strip(transit_port), transit_port_en=safe_strip(transit_port_en),
            company=safe_strip(company), company_en=safe_strip(company_en), route=safe_strip(route),
            duration=safe_to_int(duration), currency_unit=safe_strip(currency_unit),
            valid_from_date=safe_strip(valid_from_date), valid_to_date=safe_strip(valid_to_date),
            date_cut_off=safe_strip(date_cut_off), date_set_sail=safe_strip(date_set_sail),
            price_20gp=safe_to_int(price_20gp), price_40gp=safe_to_int(price_40gp), price_40hq=safe_to_int(price_40hq)
        )
