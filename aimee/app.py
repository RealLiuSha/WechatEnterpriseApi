# -*- coding:utf-8 -*-
# Author:      LiuSha
from flask import (
    g,
    Flask,
    request,
    jsonify
)

from flask_restful import (
    Api
)

import os
import time
import logging.handlers

from .model import db
from .config import LOG_PATH
from .common import WechatUtils


#: for import *
__all__ = ['app_init']


def app_init(config=None):
    """ Create Flask App """
    app = Flask(__name__)
    app.config.from_pyfile("config.py")

    #: Flask Restful
    api = Api(app)

    if isinstance(config, dict):
        app.config.update(config)
    elif config:
        app.config.from_pyfile(os.path.abspath(config))

    register_database(app)
    register_hooks(app)
    register_routes(api)
    register_logging(app)

    return app


def register_database(app):
    db.init_app(app)
    db.app = app


def register_hooks(app):
    """Hooks for request."""

    @app.errorhandler(Exception)
    def all_exception_handler(error):
        app.logger.error("exception: %s" % error)
        return jsonify(**{
            'status': 'Oh Shit',
            'desc': str(error),
            'endpoint': request.endpoint
        }), 500

    @app.before_request
    def before_request_handler():
        g.before_request_time = time.time()
        g.wx_token = WechatUtils.auth_token().get('token')

    @app.after_request
    def after_request_handler(response):
        if hasattr(g, '_before_request_time'):
            delta = time.time() - g.before_request_time
            response.headers['Server'] = 'AimeeWS'
            response.headers['X-Render-Time'] = delta * 1000

        #: cross-origin
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')

        return response


def register_routes(api):
    from .handlers import (
        ApiDefault,
        Wechat,
        WechatVerify,
        WechatUser,
        WechatSend,
        WechatGroup,
        PrometheusApi
    )
    api.add_resource(ApiDefault, '/')
    api.add_resource(Wechat, '/api/<string:app_name>')
    api.add_resource(WechatVerify, '/api/<string:app_name>/verify')
    api.add_resource(WechatUser, '/api/<string:app_name>/user')
    api.add_resource(WechatSend, '/api/<string:app_name>/send')
    api.add_resource(WechatGroup, '/api/group')
    api.add_resource(PrometheusApi, '/api/prometheus')


def register_logging(app):
    if app.debug:
        return

    app.logger.setLevel(logging.INFO)
    info_file_handler = logging.handlers.RotatingFileHandler(
        LOG_PATH, maxBytes=100000, backupCount=10
    )

    info_file_handler.setLevel(logging.INFO)
    info_file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]')
    )

    app.logger.addHandler(info_file_handler)

    #: Testing
    """
    #app.logger.info("testing info.")
    app.logger.warn("testing warn.")
    app.logger.error("testing error.")
    """
