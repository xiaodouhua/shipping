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


class ItemBfb56(Item):
    uid = Field()
    starting_port = Field()
    starting_port_en = Field()
    destination_port = Field()
    destination_port_en = Field()
    company = Field()
    valid_date = Field()
    duration = Field()
    schedule = Field()
    cargo_type = Field()
    price_20gp = Field()
    price_40gp = Field()
    price_40hq = Field()
    url = Field()


class ItemUfsoo(Item):
    uid = Field()
    starting_port = Field()
    starting_port_en = Field()
    destination_port = Field()
    destination_port_en = Field()
    transit_port = Field()
    transit_port_en = Field()
    route = Field()
    company = Field()
    company_en = Field()
    duration = Field()
    date_cut_off = Field()
    date_set_sail = Field()
    valid_from_date = Field()
    valid_to_date = Field()
    currency_unit = Field()
    price_20gp = Field()
    price_40gp = Field()
    price_40hq = Field()
