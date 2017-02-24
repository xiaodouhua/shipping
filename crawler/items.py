from scrapy import Item, Field


class ItemWlg(Item):
    uid = Field()
    starting_port = Field()
    destination_port = Field()
    transit_port = Field()
    wharf = Field()
    route = Field()
    company = Field()
    date_cut_off = Field()
    date_set_sail = Field()
    week_cut_off = Field()
    week_set_sail = Field()
    duration = Field()
    price_20gp = Field()
    price_40gp = Field()
    price_40hq = Field()


class ItemJc56(Item):
    uid = Field()
    starting_port = Field()
    destination_port = Field()
    transit_port = Field()
    route = Field()
    company = Field()
    duration = Field()
    schedule = Field()
    valid_from_date = Field()
    valid_to_date = Field()
    price_20gp = Field()
    price_40gp = Field()
    price_40hq = Field()
    surcharge = Field()
    remarks = Field()
