#!/usr/bin/env python
#-*-coding=utf-8-*-
#
#File Name: ".expand("%"))
#Copyright(c) 2015-2024 Beijing Carryon.top Corp.
#
#Author LiuBin on: Sat Apr  7 11:36:32 CST 2018
#
#@desc:
#
#@history
#

import json
from django.test import TestCase
# from selenium import webdriver
from weixin.proxy import TokenGetter, UserAPI

# Create your tests here.

class WeixinTestCase(TestCase):
    """
    测试微信接口
    """
    def setUp(self):
        # 往测试数据库中插入数据，以便测试取用本地token是否有效
        tg = TokenGetter()
        token = tg.get_token()
        token.save()

    def test_user_api(self):
        """
        """
        tg = TokenGetter(appid='wx4a32725dfd171687', appsecret='14123aca2110ec62e097ab8c1cb2734d')
        token = tg.get_token()
        print('use token: ', token.access_token)
        user_api = UserAPI(token.access_token)
        r = user_api.get_user_list()
        # user_list = json.loads(r.content.decode())
        user_list = r.json()
        print(user_list)
        self.assertEqual(r.ok, True)
        self.assertEqual(r.status_code, 200)


    def test_user_list_view(self):
        pass
