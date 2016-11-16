# -*- coding:utf-8 -*-
# Author:      LiuSha

import datetime
from flask_sqlalchemy import SQLAlchemy, BaseQuery

__all__ = [
    'db', 'AimeeQuery', 'SessionMixin', 'format_unix_time'
]


def format_unix_time(_value):
    if not _value:
        return None
    return datetime.datetime.fromtimestamp(int(_value)).strftime('%Y-%m-%d %H:%M')


class AimeeQuery(BaseQuery):
    def filter_in(self, model, values):
        values = set(values)
        if len(values) == 0:
            return {}
        if len(values) == 1:
            ident = values.pop()
            rv = self.get(ident)
            if not rv:
                return {}
            return {ident: rv}
        items = self.filter(model.in_(values))
        dct = {}
        for item in items:
            dct[getattr(item, model.key)] = item
        return dct

    def as_list(self, *columns):
        return self.options(map(db.defer, columns))


class SessionMixin(object):
    def to_dict(self, *columns):
        dct = {}
        for col in columns:
            value = getattr(self, col)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%Y-%m-%d %H:%M:%S')
            dct[col] = value
        return dct

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self


db = SQLAlchemy()
db.Model.query_class = AimeeQuery
