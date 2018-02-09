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


class BaseBackend(object):
    """
    实现基础的跳转第三方AOUTH2登录页、获取ACCESS_TOKEN、刷新ACCESS_TOKEN、
    获取用户信息、检验授权凭证是否有效等功能
    """
    _APPID = None
    _BACKEND = None
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

    def get_access_token(self, code=None):
        """
        根据第三方名称及用户授权后给的code从第三方获取进一步的access_token
        """
        if code is None:
            raise
