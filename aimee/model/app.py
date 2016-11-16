# -*- coding:utf-8 -*-
# Author:      LiuSha

from ._base import db, SessionMixin

from flask_restful import (
    marshal,
    fields
)

__all__ = ['Apps']


class Apps(db.Model, SessionMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    app_id = db.Column(db.CHAR(16), nullable=False)
    app_name = db.Column(db.VARCHAR(64), primary_key=True, nullable=False)
    app_desc = db.Column(db.VARCHAR(64), nullable=False)
    app_key = db.Column(db.CHAR(255), nullable=False)
    app_token = db.Column(db.CHAR(255), nullable=False)

    def __str__(self):
        return self.id

    def __repr__(self):
        return '<Apps: %s>' % self.app_name

    @staticmethod
    def to_dict(data):
        if isinstance(None, type(data)):
            return None

        _fields = {
            'id': fields.String, 'app_id': fields.String,
            'app_name': fields.String, 'app_desc': fields.String,
            'app_key': fields.String, 'app_token': fields.String,
        }

        return dict(marshal(data, _fields))

    @staticmethod
    def get(_app_name):
        apps = Apps.query.filter(Apps.app_name == _app_name).first()
        return Apps.to_dict(apps)

    @staticmethod
    def add(query_data):
        logs = Apps(**query_data)
        logs.save()

    @staticmethod
    def update(query_data):
        app_name = query_data.pop('app_name')
        apps = Apps.query.filter(Apps.app_name == app_name).first()
        for key, value in query_data.items():
            setattr(apps, key, value)

        apps.save()

    @staticmethod
    def remove(_app_name):
        apps = Apps.query.filter(Apps.app_name == _app_name).first()
        apps.delete()
