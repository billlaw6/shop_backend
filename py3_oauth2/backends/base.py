#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# File Name: ".expand("%"))
# Copyright(c) 2015-2024 Beijing Carryon.top Corp.
#
# Author LiuBin on: Fri Feb  9 14:55:04 CST 2018
#
# @desc: 用于微信、微博、QQ等第三方系统登录
#
# @history
#

import requests
from ../errors import MissingCodeError


class BaseBackend(object):
    """
    实现基础的跳转第三方AOUTH2登录页、获取ACCESS_TOKEN、刷新ACCESS_TOKEN、
    获取用户信息、检验授权凭证是否有效等功能
    """
    _APPID = None
    _BACKEND = None
    _
    # _REDIRECT_URI = None
    # _RESPONSE_TYPE = None
    # _SCOPE = None
    # _STATE = None

    def __init__(self, appid=None, backend=None):
        """
        传入参数为第三方提供的appID（如微信）或App Key（如微博）以及第三方名称
        拼音，方便找对应的类处理。
        """
        self._APPID = appid
        self._BACKEND = backend

    def _get_authorize_uri(self):
        """
        点击第三方登录链接后，系统跳转的基础地址。
        如微信的：
        https://open.weixin.qq.com/connect/oauth2/authorize
        用户同意后再跳转到指定的REDIRECT_URI，系统从这次访问中获取code和state,
        然后进一步用code换取access_token和refresh_token
        不同第三方的地址不一样，地址太长也不方便放到__init__中，所以放函数中
        各自定义
        """
        raise NotImplementedError('_get_authorize_uri未实现')

    def _get_complete_login_uri(self):
        """
        应该是本模块用code获取授权信息的地址，即用户同意后再跳转的REDIRECT_URI，
        系统从这次访问中获取code和state，这里根据不同第三方返回相应标准化的URI
        如：complete_social_login/weixin
        访问此地址后应该完成第三方登录操作，新的openid还应该创建系统用户
        """
        raise NotImplementedError('_get_complete_login_uri未实现')

    def _get_access_token_uri(self):
        """
        应该是本模块用code获取授权信息的地址，即用户同意后再跳转的REDIRECT_URI，
        系统从这次访问中获取code和state，这里根据不同第三方返回相应标准化的URI
        如：complete_social_login/weixin
        不同第三方的地址不一样，地址太长也不方便放到__init__中，所以放函数中
        各自定义
        """
        raise NotImplementedError('_get_access_token_uri未实现')

    def _get_refresh_token_uri(self):
        """
        用refresh_token换取新access_token地址
        不同第三方的地址不一样，地址太长也不方便放到__init__中，所以放函数中
        各自定义
        """
        raise NotImplementedError('_get_refresh_token_uri未实现')

    def _get_user_info_uri(self):
        """
        用access_token获取用户信息URI
        不同第三方的地址不一样，地址太长也不方便放到__init__中，所以放函数中
        各自定义
        """
        raise NotImplementedError('_get_user_info_uri未实现')

    def get_access_token(self, code=None, backend=None):
        """
        供complete_social_login/backend地址调用，根据backend获取对应的appid,
        secret, grant_type，结合code参数
        根据第三方名称及用户授权后给的code从第三方获取进一步的access_token
        """
        if code is None:
            raise MissingCodeError('get_access_token中code为空')
        params = {}
        appid=''

        res = request(
