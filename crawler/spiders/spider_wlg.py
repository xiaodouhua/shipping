import json
import scrapy
import math
import logging
from scrapy import FormRequest, Selector
from items import ItemWlg

logger = logging.getLogger('SpiderWlg')


class SpiderWlg(scrapy.Spider):
    name = "wlg"  # http://www.e-wlg.com/

    def start_requests(self):
        yield self.make_request()

    def parse(self, response):
        data = json.loads(response.body.decode(response.encoding))
        count = data['fclfCount']

        # all_routes = data['line']  # 航线
        # all_companies = data['ship']  # 公司
        sb = data['sb']  # 报价

        for record in Selector(text=sb).xpath('//div[@id="main-booking2"]'):
            try:
                yield self.parse_record(record)
            except ValueError as e:
                logger.error(e)
                continue

        page = response.meta['page']
        if page == 0:
            for i in range(1, math.ceil(count / 10.0)):
                yield self.make_request(i)

    def parse_record(self, record):
        def safe_cast_price(s):
            try:
                return int(s.replace('$', '').strip())
            except (ValueError, TypeError):
                return None

        starting_port = record.xpath('div[2]/ul/li[2]/div/div[1]/div[2]/text()').extract_first()
        starting_port = starting_port.strip() if starting_port else None

        destination_port = record.xpath('div[2]/ul/li[2]/div/div[3]/text()').extract_first()
        destination_port = destination_port.strip() if destination_port else None

        transit_port = None
        method = record.xpath('div[2]/ul/li[2]/div/div[2]/text()').extract_first()
        if method is not None and method.find('中转') >= 0:
            transit_port = method.replace('中转', '').strip()

        price = record.xpath('div[2]/ul/li[3]/div/div[@class="yunred yunlist"]/text()')
        price_20gp = safe_cast_price(price[0].extract())
        price_40gp = safe_cast_price(price[1].extract())
        price_40hq = safe_cast_price(price[2].extract())

        company = record.xpath('div[2]/ul/li[4]/text()[1]').extract_first()
        company = company.strip() if company else None

        route = record.xpath('div[2]/ul/li[4]/text()[1]').extract_first()
        route = route.strip() if route else None

        wharf = record.xpath('div[2]/ul/li[5]/text()').extract_first()
        wharf = wharf.strip() if wharf else None

        cut_off = record.xpath('div[2]/ul/li[6]/p[1]/text()').extract_first()

        if cut_off:
            cut_off = cut_off.split('|')
            date_cut_off = cut_off[0].strip()
            week_cut_off = cut_off[1].strip()
        else:
            date_cut_off = None
            week_cut_off = None

        set_sail = record.xpath('div[2]/ul/li[6]/p[2]/text()').extract_first()
        if set_sail:
            set_sail = set_sail.split('|')
            date_set_sail = set_sail[0].strip()
            week_set_sail = set_sail[1].strip()
        else:
            date_set_sail = None
            week_set_sail = None

        duration = record.xpath('div[2]/ul/li[7]/text()').extract_first()
        duration = int(duration.replace('天', '').strip()) if duration else None

        uid = record.xpath('.').re_first('id="(WLYJ.*?)"').strip()

        return ItemWlg(
            uid=uid, starting_port=starting_port,
            destination_port=destination_port, transit_port=transit_port,
            company=company, route=route, wharf=wharf, duration=duration,
            date_cut_off=date_cut_off, date_set_sail=date_set_sail,
            week_cut_off=week_cut_off, week_set_sail=week_set_sail,
            price_20gp=price_20gp, price_40gp=price_40gp, price_40hq=price_40hq
        )

    def make_request(self, page=0):
        url = 'http://www.e-wlg.com/web/nb_fcl/freight?' \
              'p_p_id=fclfreightquery_WAR_smartwlgfclbookingportlet&' \
              'p_p_lifecycle=2&' \
              'p_p_state=normal&' \
              'p_p_mode=view&' \
              'p_p_cacheability=cacheLevelPage&' \
              'p_p_col_id=column-1&' \
              'p_p_col_count=1'

        form_data = {
            '_fclfreightquery_WAR_smartwlgfclbookingportlet_basepath': 'http://www.e-wlg.com:80/smart-wlg-fcl-booking-portlet/',
            'fclfreightqueryURL': 'http://www.e-wlg.com/web/nb_fcl/freight?'
                                  'p_p_id=smartwlgorder_WAR_smartwlgorderportlet&'
                                  'p_p_lifecycle=0&'
                                  'p_p_state=pop_up&'
                                  'p_p_mode=view&'
                                  'p_p_col_id=column-1&'
                                  'p_p_col_count=1&'
                                  '_smartwlgorder_WAR_smartwlgorderportlet_fclfCode=1&'
                                  '_smartwlgorder_WAR_smartwlgorderportlet_isZk=-1',
            'p_p_resource_id': 'query',
            '_fclfreightquery_WAR_smartwlgfclbookingportlet_pageIndex': str(page),  # 从0开始
            '_fclfreightquery_WAR_smartwlgfclbookingportlet_shipcompanyCode': '',
            '_fclfreightquery_WAR_smartwlgfclbookingportlet_lineName': '',
            '_fclfreightquery_WAR_smartwlgfclbookingportlet_isdirect': '',
            '_fclfreightquery_WAR_smartwlgfclbookingportlet_closeDay': '',
            '_fclfreightquery_WAR_smartwlgfclbookingportlet_destinationportName': '',
            '_fclfreightquery_WAR_smartwlgfclbookingportlet_desportCountryCname': '',
            'startportName': 'NINGBO',
            'order_yj': '',
            'order_hc': '',
            'toGroup': 'http://www.e-wlg.com/web/nb_fcl/freight?'
                       'p_auth=wOhaeJjz&'
                       'p_p_id=fclfreightquery_WAR_smartwlgfclbookingportlet&'
                       'p_p_lifecycle=1&'
                       'p_p_state=normal&'
                       'p_p_mode=view&'
                       'p_p_col_id=column-1&'
                       'p_p_col_count=1&'
                       '_fclfreightquery_WAR_smartwlgfclbookingportlet_javax.portlet.action=toGroup'
        }

        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2,ja;q=0.2',
            'Referer': 'http://www.e-wlg.com/web/nb_fcl/freight?STARTPORT=&SHIPCOMPANY=&ENDPORT=&desportCountryCname=',
            'Origin': 'http://www.e-wlg.com',
            'X-Requested-With': 'XMLHttpRequest'
        }

        return FormRequest(url, formdata=form_data, headers=headers, meta={'page': page})
