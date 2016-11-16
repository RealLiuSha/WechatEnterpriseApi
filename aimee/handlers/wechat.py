# -*- coding:utf-8 -*-
# Author:      LiuSha
# Email:       itchenyi@gmail.com
from flask_restful import (
    Resource,
    reqparse
)

from flask import (
    g,
    make_response
)

from ..model import (
    Apps,
    Logs
)

from ..common import WechatUtils


class Wechat(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('app_desc', required=True, help="required app_desc", location="json")
        self.parser.add_argument('app_id', required=True, help="required app_id", location="json")
        self.parser.add_argument('app_key', required=True, help="required app_key", location="json")
        self.parser.add_argument('app_token', required=True, help="required app_token", location="json")

    @classmethod
    def get(cls, app_name):
        WechatUtils.app_doesnt_exist(app_name)
        app_detail = Apps.get(app_name)

        return app_detail

    def post(self, app_name):
        WechatUtils.app_doesnt_exist(app_name)
        req_args = self.parser.parse_args()
        req_args['app_name'] = app_name

        Apps.update(req_args)

        return Apps.get(app_name)

    def put(self, app_name):
        WechatUtils.app_already_exist(app_name)
        req_args = self.parser.parse_args()
        req_args['app_name'] = app_name

        Apps.add(req_args)

        return {'message': 'success'}

    @classmethod
    def delete(cls, app_name):
        WechatUtils.app_doesnt_exist(app_name)
        Apps.remove(app_name)

        return {'message': 'success'}


class WechatVerify(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('nonce', help="required nonce", location='args')
        self.parser.add_argument('echostr', help="required echostr", location='args')
        self.parser.add_argument('timestamp', help="required timestamp", location='args')
        self.parser.add_argument('msg_signature', help="required msg_signature", location='args')

    def get(self, app_name):
        req_args = self.parser.parse_args()
        app_detail = Apps.get(app_name)

        req_args.update(app_detail)

        return make_response(WechatUtils.verify(req_args))


class WechatSend(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('touser', help="required touser", location='json')
        self.parser.add_argument('toparty', help="weixinid toparty", location='json')
        self.parser.add_argument('text', help="required text", location='json')
        self.parser.add_argument('source', help="required source", location='json')

    def put(self, app_name):
        app_detail = Apps.get(app_name)
        req_args = self.parser.parse_args()
        req_args['safe'] = 0
        req_args['msgtype'] = "text"
        req_args['wx_token'] = g.wx_token
        req_args['agentid'] = app_detail['app_id']
        msg_content = '%s:\n%s' % (req_args['source'], req_args['text'])
        req_args['text'] = {'content': msg_content}

        Logs.add({'text': msg_content, 'app_name': app_name})

        if not req_args['toparty']:
            req_args.pop('toparty')

        return WechatUtils.send(req_args)


class WechatUser(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', help="required name", location='json')
        self.parser.add_argument('weixinid', help="weixinid userid", location='json')
        self.parser.add_argument('department', type=list, help="required department", location='json')

        self.delete_parser = reqparse.RequestParser()
        self.delete_parser.add_argument('weixinid', help="weixinid userid", location='json')

    @classmethod
    def get(cls, app_name):
        WechatUtils.app_doesnt_exist(app_name)
        app_detail = Apps.get(app_name)
        app_detail['wx_token'] = g.wx_token
        return WechatUtils.user_list(app_detail)

    def put(self, app_name):
        WechatUtils.app_doesnt_exist(app_name)
        req_args = self.parser.parse_args()
        req_args['wx_token'] = g.wx_token
        req_args['userid'] = req_args['weixinid']

        return WechatUtils.add_user(req_args)

    def post(self, app_name):
        WechatUtils.app_doesnt_exist(app_name)
        req_args = self.parser.parse_args()
        req_args['wx_token'] = g.wx_token
        req_args['userid'] = req_args['weixinid']

        return WechatUtils.update_user(req_args)

    def delete(self, app_name):
        WechatUtils.app_doesnt_exist(app_name)
        req_args = self.delete_parser.parse_args()
        req_args = {
            'wx_token': g.wx_token,
            'userid': req_args.pop('weixinid')
        }

        return WechatUtils.delete_user(req_args)


class WechatGroup(Resource):

    @staticmethod
    def get():
        return WechatUtils.group_list({'wx_token': g.wx_token})
