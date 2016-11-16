# -*- coding:utf-8 -*-
# Author:      LiuSha
# Email:       itchenyi@gmail.com
from flask_restful import (
    Resource
)


class ApiDefault(Resource):
    @classmethod
    def get(cls):
        return {'message': 'hello, i am aimee...'}
