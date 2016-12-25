import datetime

from peewee import *

db = SqliteDatabase('entries.db')


class Entry(Model):
    entry = TextField()
    timestamp = DateTimeField(default=datetime.datetime.now)
    state = CharField(default='inbox')
    workspace = TextField()

    class Meta:
        database = db
        order_by = ('-timestamp',)

class Workspace(Model):
    workspace = TextField()
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db
        order_by = ('-timestamp',)

def initialize():
    db.connect()
    db.create_tables([Entry, Workspace], safe=True)
    db.close()
