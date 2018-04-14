#!/usr/bin/env python
#-*-coding=utf-8-*-
#
#File Name: ".expand("%"))
#Copyright(c) 2015-2024 Beijing Carryon.top Corp.
#
#Author LiuBin on: Tue Mar 27 20:33:24 CST 2018
#
#@desc: 为了不暴露access_token，不能把微信API在前端调用，所以在后端封装一下
#
#@history
#


import time
import json
import hashlib
from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from django.utils.encoding import smart_str
from django.views.decorators.csrf import csrf_exempt
from weixin.proxy import TokenGetter, MessageEventHandler, MessageAPI, UserAPI


# Create your views here.
class WeChatAutoReply(View):
    """
    普通用户向公众号发消息时，微信服务器将POST消息的XML数据包到公众号填写的URL上
    """
    # https://code.djangoproject.com/ticket/15794
    # 只能放在dispatch上，放POST上不一定灵
    # @method_decorator(csrf_exempt)
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(WeChatAutoReply, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        """
        纯用于微信服务器校验
        """
        token = 'carryontop'
        timestamp = request.GET.get('timestamp', 'timestamp')
        nonce = request.GET.get('nonce', 'nonce')
        signature = request.GET.get('signature', 'signature')
        echostr = request.GET.get('echostr', 'echostr')
        tmp_arr = sorted([timestamp, nonce, token])
        tmp_str = ''.join(tmp_arr)
        hash_str = hashlib.sha1(tmp_str.encode("utf8"))
        # print(hash_str.hexdigest())
        if signature == hash_str.hexdigest():
            return HttpResponse(echostr)
        else:
            return HttpResponse('no match')

    def post(self, request, *args, **kwargs):
        """
        处理用户发送的消息
        """
        # print(request.body.decode('utf-8'))
        # 将获取到的非unicode字符转换为可处理的字符编码
        data = smart_str(request.body)
        msg_handler = MessageEventHandler()
        msg = msg_handler.parse_msg_event(data)
        paras = {}
        # paras.update(msg)
        paras['to_user'] = msg['from_user']
        paras['from_user'] = msg['to_user']
        paras['create_time'] = int(time.time())
        paras['content'] = '试试就试试'
        paras['media_id'] = ''
        message = msg_handler.get_text_msg(paras)
        # print(message)
        return HttpResponse(message, content_type='application/xml')


class WeChatMenu(View):
    """
    微信公众号菜单页
    """
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(WeChatMenu, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        """
        """
        print("menu 1")
        return render(request, 'index.html')


class UserList(View):
    """
    返回json格式的关注了公众号的用户openid列表
    """
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(UserList, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        返回用户列表
        """
        tg = TokenGetter()
        user_api = UserAPI(tg.get_token().access_token)
        user_list = user_api.get_user_list()
        return HttpResponse(user_list, content_type='application/json')

    def get(self, request, *args, **kwargs):
        """
        返回用户列表
        """
        tg = TokenGetter()
        user_api = UserAPI(tg.get_token().access_token)
        user_list = user_api.get_user_list()
        return HttpResponse(user_list, content_type='application/json')


class UserInfo(View):
    """
    返回json格式的具体openid用户的信息
    """
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(UserInfo, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        """
        返回用户基本信息
        """
        data = json.loads(request.body.decode())
        # print('received openid: ', data['openid'])
        tg = TokenGetter()
        user_api = UserAPI(tg.get_token().access_token)
        user_info= user_api.get_user_info(openid=data['openid'])
        return HttpResponse(user_info, content_type='application/json')

    def post(self, request, *args, **kwargs):
        """
        返回用户基本信息
        """
        data = json.loads(request.body.decode())
        # print('received openid: ', data['openid'])
        tg = TokenGetter()
        user_api = UserAPI(tg.get_token().access_token)
        user_info= user_api.get_user_info(openid=data['openid'])
        return HttpResponse(user_info, content_type='application/json')


class BatchUserInfo(View):
    """
    返回json格式的指定openid列表中公众号的用户信息
    """
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(BatchUserInfo, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        返回指定用户openid列表的用户基本信息
        """
        data = json.loads(request.body.decode())
        print(data)
        total = data['total']
        count = data['count']
        openid_data = data['data']
        next_openid = data['next_openid']
        # print(type(openid_data))
        # print(openid_data['openid'])
        paras = []
        for openid in openid_data['openid']:
            tmp_openid = {'openid': openid}
            tmp_openid['lang'] = 'zh_CN'
            print(tmp_openid)
            paras.append(tmp_openid)
        openid_list = {'user_list': paras}
        print(openid_list)
        json_paras = json.dumps(openid_list, ensure_ascii=False)
        tg = TokenGetter()
        user_api = UserAPI(tg.get_token().access_token)
        user_list = user_api.batchget_user_info(json_data=json_paras)
        return HttpResponse(user_list, content_type='application/json')

    def get(self, request, *args, **kwargs):
        """
        返回指定用户openid列表的用户基本信息
        """
        data = json.loads(request.body.decode())
        total = data['total']
        count = data['count']
        data = data['data']
        next_openid = data['next_openid']
        print(data)
        print(data['openid'])
        tg = TokenGetter()
        user_api = UserAPI(tg.get_token().access_token)
        user_list = user_api.batchget_user_info(json_data=paras)
        return HttpResponse(user_list, content_type='application/json')
