# -*- coding:utf-8 -*-
# Author:      LiuSha
from flask_restful import (
    Resource,
    reqparse
)

from flask import g, request, json
from ..common import WechatUtils
from ..model import Apps, Logs

__all__ = ['PrometheusApi']


class PrometheusApi(Resource):
    """
    Prometheus Alert Api
    """
    def __init__(self):
        self.post_parser = reqparse.RequestParser()
        self.post_parser.add_argument("alerts", required=True, type=list, help="required alerts", location="json")
        self.post_parser.add_argument("status", required=True, help="required status", location="json")

    def post(self):
        req_args = self.post_parser.parse_args()
        if not req_args:
            return {'message': 'bad request.'}, 400

        app_detail = Apps.get('devops')
        req_args['safe'] = 0
        req_args['touser'] = 'jack|laelli|lesfly|freedie|jamesqin|liubin'
        req_args['toparty'] = ''
        req_args['msgtype'] = "text"
        req_args['wx_token'] = g.wx_token
        req_args['agentid'] = app_detail['app_id']
        msg_template = (
            '任务: {job_name}\n'
            '级别: {severity}\n'
            '描述: {description}'
        )
        msg_content, annotations = [], {}
        for item in req_args['alerts']:
            if not item.get('annotations'):
                continue
            if item['labels']['job'] not in annotations:
                annotations[item['labels']['job']] = 0
                msg_content.append(msg_template.format(
                    job_name=item['labels'].get('job'),
                    status=item.get('status'),
                    severity=item['labels'].get('severity'),
                    description=item['annotations']['description']
                ))
            else:
                annotations[item['labels']['job']] += 1

        annotations_content = [
            '注意: 任务{k}还有{v}条通知由于类型相同被合并.'.format(k=k, v=annotations[k])
            for k in annotations.keys()
            if annotations.get(k) >= 1
        ]

        if annotations_content:
            msg_content.append(annotations_content.pop())

        msg_content = '\n\n'.join(msg_content)
        req_args['text'] = {'content': msg_content}

        Logs.add({'text': msg_content, 'app_name': 'devops'})

        if not req_args['toparty']:
            req_args.pop('toparty')

        WechatUtils.send(req_args)

        return {'message': 'done.'}, 200

