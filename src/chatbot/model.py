# -*- coding: utf-8 -*-

"""
Model for SQL storage for logging

"""

import datetime
import sqlalchemy as sql


__all__ = ["messages", "tags", "urls", "quotes", "engine", "use_engine"]


meta = sql.MetaData()

messages = sql.Table("messages", meta,
    sql.Column("id", sql.Integer, primary_key=True, autoincrement=True),
    sql.Column("chat", sql.Unicode, index=True), 
    sql.Column("skype_message_id", sql.Integer),
    sql.Column("skype_timestamp", sql.DateTime),
    sql.Column("from_name", sql.Unicode, index=True),
    sql.Column("from_handle", sql.Unicode, index=True),
    sql.Column("body", sql.Unicode),
    sql.Column("created", sql.DateTime, default=datetime.datetime.now)
)

tags = sql.Table("message_tags", meta, 
    sql.Column("message_id", sql.Integer, sql.ForeignKey("messages.id")), 
    sql.Column("tag", sql.Unicode),
    sql.Column("created", sql.DateTime, default=datetime.datetime.now),
    sql.PrimaryKeyConstraint("message_id", "tag")
)

urls = sql.Table("message_urls", meta,
    sql.Column("message_id", sql.Integer, sql.ForeignKey("messages.id")), 
    sql.Column("url", sql.Unicode),
    sql.Column("created", sql.DateTime, default=datetime.datetime.now),
    sql.PrimaryKeyConstraint("message_id", "url")
)

phrases = sql.Table("phrases", meta, 
    sql.Column("id", sql.Integer, primary_key=True, autoincrement=True),
    sql.Column("type", sql.Integer),
    sql.Column("phrase", sql.Unicode)
)

quotes = sql.Table("quotes", meta, 
    sql.Column("id", sql.Integer, primary_key=True, autoincrement=True),
    sql.Column("quote", sql.Unicode)
)

engine = None

def use_engine(engine_to_use, create_all=True):
    global engine
    engine = engine_to_use
    if create_all:
    	meta.create_all(engine)

