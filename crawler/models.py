import datetime
from peewee import Model, MySQLDatabase, IntegerField, DateField, CharField, TextField, DateTimeField

db = MySQLDatabase('shipping', host="localhost", port=3306, user="root", passwd="19961020")


class BaseModel(Model):
    class Meta:
        database = db


class TableWlg(BaseModel):
    uid = CharField(primary_key=True)
    scraped_time = DateTimeField(default=datetime.datetime.now)
    starting_port = CharField(null=True)
    destination_port = CharField(null=True)
    transit_port = CharField(null=True)
    wharf = CharField(null=True)
    route = CharField(null=True)
    company = CharField(null=True)
    date_cut_off = DateField(null=True)
    date_set_sail = DateField(null=True)
    week_cut_off = CharField(null=True)
    week_set_sail = CharField(null=True)
    duration = IntegerField(null=True)
    price_20gp = IntegerField(null=True)
    price_40gp = IntegerField(null=True)
    price_40hq = IntegerField(null=True)

    class Meta:
        db_table = 'wlg'


class TableJc56(BaseModel):
    uid = IntegerField(primary_key=True)
    scraped_time = DateTimeField(default=datetime.datetime.now)
    starting_port = CharField(null=True)
    destination_port = CharField(null=True)
    transit_port = CharField(null=True)
    route = CharField(null=True)
    company = CharField(null=True)
    duration = IntegerField(null=True)
    schedule = CharField(null=True)
    valid_from_date = CharField(null=True)
    valid_to_date = CharField(null=True)
    price_20gp = IntegerField(null=True)
    price_40gp = IntegerField(null=True)
    price_40hq = IntegerField(null=True)
    surcharge = CharField(null=True)
    remarks = TextField(null=True)

    class Meta:
        db_table = 'jc56'


def create_tables():
    db.create_tables([TableWlg, TableJc56], safe=True)
