# -*- coding:utf-8 -*-
# Author:      LiuSha
# Email:       itchenyi@gmail.com
import os

#: db config
DATABASE = {
    'db': "",
    'user': "",
    'host': '',
    'port': 3306,
    'passwd': '',
    'charset': 'utf8'
}

#: sqlalchemy
SQLALCHEMY_DATABASE_URI = (
    'mysql+pymysql://'
    '{user}:{passwd}@{host}/{db}?charset={charset}'
).format(**DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = True

#: app config
SECRET_KEY = "secret-key"
SESSION_COOKIE_NAME = "_aimee"
PERMANENT_SESSION_LIFETIME = 3600 * 24 * 30
SITE_COOKIE = "Interesting"
HTTP_PORT = 8087
HTTP_HOST = '0.0.0.0'

WX_URL = {
    'Token': 'https://qyapi.weixin.qq.com/cgi-bin/gettoken',
    'UserList': 'https://qyapi.weixin.qq.com/cgi-bin/user/list',
    'SendMsg': 'https://qyapi.weixin.qq.com/cgi-bin/message/send',

    #: For User Op
    'UserCreate': 'https://qyapi.weixin.qq.com/cgi-bin/user/create',
    'UserUpdate': 'https://qyapi.weixin.qq.com/cgi-bin/user/update',
    'UserGet': 'https://qyapi.weixin.qq.com/cgi-bin/user/get',
    "UserDelete": "https://qyapi.weixin.qq.com/cgi-bin/user/delete",

    #: For Group Op
    'GroupList': 'https://qyapi.weixin.qq.com/cgi-bin/department/list'
}


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_PATH = os.path.join(BASE_DIR, "var", "info.log")

#: WX CONFIG
WX_CORP_ID = ''
WX_SECRET = ''
WX_TOKEN_PATH = os.path.join(BASE_DIR, 'var', '.wx_token.json')
