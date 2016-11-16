# -*- coding:utf-8 -*-
# Author:      LiuSha

from datetime import datetime
from ._base import db, SessionMixin

__all__ = ['Logs']


class Logs(db.Model, SessionMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.Text, nullable=False)
    app_name = db.Column(db.VARCHAR(64), nullable=False)
    create_at = db.Column(db.DATETIME, index=True, default=datetime.now(), nullable=False)

    def __str__(self):
        return self.jid or self.aid

    def __repr__(self):
        return '<Jobs: %s>' % self.jid

    @staticmethod
    def add(query_data):
        logs = Logs(**query_data)
        logs.save()
