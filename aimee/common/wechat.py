# -*- coding:utf-8 -*-
# Author:      LiuSha
# Email:       itchenyi@gmail.com
from ._wx_encrypt.WXBizMsgCrypt import (
    WXBizMsgCrypt
)

from aimee.config import (
    WX_URL,
    WX_SECRET,
    WX_CORP_ID,
    WX_TOKEN_PATH
)

from ._http import HttpUtils
from ..model import Apps
from flask_restful import abort

import os
import json
from time import time as unix_time


class WechatUtils(object):
    @classmethod
    def verify(cls, data):
        print(data)
        wx_crypt = WXBizMsgCrypt(
            sToken=data['app_token'],
            sEncodingAESKey=data['app_key'],
            sAppId=WX_CORP_ID
        )

        result, echo_str = wx_crypt.VerifyURL(
            sMsgSignature=data['msg_signature'],
            sNonce=data['nonce'],
            sTimeStamp=data['timestamp'],
            sEchoStr=data['echostr']
        )

        if result != 0:
            return None

        return echo_str

    @classmethod
    def auth_token(cls):
        if not os.path.exists(WX_TOKEN_PATH):
            return cls.update_token()

        with open(WX_TOKEN_PATH, 'r') as _file:
            token_data = json.loads(_file.read())

        if (int(unix_time()) - token_data['timestamp']) > 7000:
            return cls.update_token()

        return token_data

    @classmethod
    def update_token(cls):
        re_code, re_data = HttpUtils.json_request(
            url=WX_URL.get('Token'),
            method='post',
            params={
                'corpid': WX_CORP_ID,
                'corpsecret': WX_SECRET
            }
        )

        HttpUtils.re_code_check(re_code, re_data)

        token_data = {
            'timestamp': int(unix_time()),
            'token': re_data['result'].get('access_token')
        }

        print(json.dumps(token_data), file=open(WX_TOKEN_PATH, 'w'))
        return token_data

    @classmethod
    def user_list(cls, data):
        re_code, re_data = HttpUtils.json_request(
            url=WX_URL['UserList'],
            method='post',
            params={
                'access_token': data['wx_token'],
                'status': 0,
                'department_id': data['app_id'],
            }
        )

        HttpUtils.re_code_check(re_code, re_data)

        return re_data.get('result', {'userlist': [{}]}).get('userlist')

    @classmethod
    def add_user(cls, data):
        wx_token = data.pop('wx_token')
        re_code, re_data = HttpUtils.json_request(
            url=WX_URL.get('UserCreate'),
            method='post',
            params={
                'access_token': wx_token
            },
            data=json.dumps(data, ensure_ascii=False).encode('utf-8')
        )

        HttpUtils.re_code_check(re_code, re_data)
        return cls.result_check(re_data)

    @classmethod
    def update_user(cls, data):
        wx_token = data.pop('wx_token')
        re_code, re_data = HttpUtils.json_request(
            url=WX_URL.get('UserUpdate'),
            method='post',
            params={
                'access_token': wx_token
            },
            data=json.dumps(data, ensure_ascii=False).encode('utf-8')
        )

        HttpUtils.re_code_check(re_code, re_data)
        return cls.result_check(re_data)

    @classmethod
    def delete_user(cls, data):
        re_code, re_data = HttpUtils.json_request(
            url=WX_URL.get('UserDelete'),
            method='get',
            params={
                'userid': data['userid'],
                'access_token': data['wx_token'],
            }
        )

        HttpUtils.re_code_check(re_code, re_data)
        return cls.result_check(re_data)

    @classmethod
    def group_list(cls, data):
        re_code, re_data = HttpUtils.json_request(
            url=WX_URL['GroupList'],
            method='post',
            params={
                'access_token': data['wx_token'],
                'id': 1
            }
        )

        HttpUtils.re_code_check(re_code, re_data)

        return re_data.get('result', {'department': [{}]}).get('department')

    @classmethod
    def send(cls, data):
        wx_token = data.pop('wx_token')
        re_code, re_data = HttpUtils.json_request(
            url=WX_URL['SendMsg'],
            method='post',
            params={
                'access_token': wx_token
            },
            data=json.dumps(data, ensure_ascii=False).encode('utf-8')
        )

        HttpUtils.re_code_check(re_code, re_data)
        return cls.result_check(re_data)

    @classmethod
    def result_check(cls, data):
        if data['result']['errcode'] == 0:
            return {'message': 'success'}

        return {'message': 'error', 'error': data['result']['errmsg']}

    @classmethod
    def app_doesnt_exist(cls, _app_name):
        result = Apps.get(_app_name)
        if not result:
            abort(400, message="app {} doesn't exist".format(_app_name))

    @classmethod
    def app_already_exist(cls, _app_name):
        if Apps.get(_app_name):
            abort(400, message="app {} is already exist".format(_app_name))
