# -*- coding:utf-8 -*-
# Author:      LiuSha
# Email:       itchenyi@gmail.com
from __future__ import (
    division,
    print_function,
    unicode_literals
)


import requests
from requests import exceptions as r_exceptions
from requests.packages.urllib3.exceptions import InsecureRequestWarning

#: Disable InsecureRequest Warning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class HttpUtils(object):
    @classmethod
    def json_request(cls, url, method, headers=None, data=None, params=None):
        """Actually make an HTTP request."""
        try:
            r = requests.request(
                url=url, method=method, headers=headers, data=data,
                params=params, verify=False)

        except r_exceptions.Timeout as err:
            return 999, {'result': 'Request Timeout.\n%s' % err}

        except r_exceptions.TooManyRedirects as err:
            return 999, {'result': 'Too many redirects.\n%s' % err}

        except r_exceptions.RequestException as err:
            return 999, {'result': 'Request Error.\n%s' % err}

        try:
            return r.status_code, {'result': r.json()}
        except ValueError as err:
            return r.status_code, {'result': 'No Json Response.\n%s' % err}

    @classmethod
    def text_request(cls, url, method, headers=None, data=None, params=None):
        try:
            r = requests.request(
                url=url, method=method, headers=headers, data=data,
                params=params, verify=False)

        except r_exceptions.Timeout as err:
            return 999, {'result': 'Request Timeout.\n%s' % err}

        except r_exceptions.TooManyRedirects as err:
            return 999, {'result': 'Too many redirects.\n%s' % err}

        except r_exceptions.RequestException as err:
            return 999, {'result': 'Request Error.\n%s' % err}

        return r.status_code, {'result': r.text}

    @classmethod
    def re_code_check(cls, _re_code, _re_data, _check_code=200):
        if _re_code != _check_code:
            raise r_exceptions.RequestException('Request Err:{}'.format(str(_re_data)))

