#!/usr/bin/env python
#-*-coding=utf-8-*-
#
#File Name: ".expand("%"))
#Copyright(c) 2015-2024 Beijing Carryon.top Corp.
#
#Author LiuBin on: Wed Mar 28 10:16:53 CST 2018
#
#@desc:
#
#@history
#

import requests
import json
import pytz
from datetime import timedelta
from datetime import datetime
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
from django.conf import settings
from weixin.exceptions import InvalidTokenException
from weixin.models import APIAccessToken


class TokenGetter(object):
    """
    微信API access_token 获取工具
    首先从本地数据库取access_token，如果过期则从微信服务器再获取
    返回APIAccessToken对象实例
    """
    def __init__(self, grant_type='client_credential', appid=settings.WEIXIN_APPID, appsecret=settings.WEIXIN_APPSECRET):
        # 默认取配置文件中的appid和appsecret
        self.grant_type = grant_type
        self.appid = appid
        self.appsecret = appsecret

    def _get_remote_token(self):
        """
        使用appid和secret从微信服务器获取access_token
        """
        url = """https://api.weixin.qq.com/cgi-bin/token"""
        payload = {'secret': self.appsecret,
                   'appid': self.appid,
                   'grant_type': self.grant_type}
        r = requests.get(url, params=payload)
        # print(r.url)
        dict_json = json.loads(r.content.decode())
        print('remote token: ', dict_json['access_token'])
        token_object = APIAccessToken(**dict_json, appid=self.appid)
        token_object.save()
        return token_object

    def _get_local_token(self):
        """
        如果本地access_token有效，返回本地access_token
        """
        try:
            print('self.appid: ', self.appid)
            token = APIAccessToken.objects.filter(appid=self.appid).latest('created_at')
            if token is not None:
                print('local token: ', token.access_token)
                return token
            else:
                return None
        # test时使用的是测试数据库，库里面没内容，所以一直走下面这段
        except APIAccessToken.DoesNotExist as e:
            print('local token does not exists: ', e)
            return None

    def get_token(self):
        """
        对外函数，自动根据本地token状态判断是否重新获取token并返回有效token
        """
        token = self._get_local_token()
        # 如果本地没有token，直接取新获得的token
        if token is None:
            token = self._get_remote_token()
            token.save()
            return token
        # 如果本地有token，本地有的话没继续判断是否过期
        # 留十秒种空错时间
        token_expires_at = token.created_at + timedelta(seconds=(token.expires_in - 10))
        token_expires_at = token_expires_at.replace(tzinfo=pytz.timezone('UTC'))
        now = datetime.now().replace(tzinfo=pytz.timezone('UTC'))
        if token_expires_at > now:
            print('return local token')
            return token
        else:
            print('local token expired')
            token = self._get_remote_token()
            return token


class MessageEventHandler(object):
    """
    解析微信XML格式消息，返回字典类型的解析结果
    或者
    根据参数生成不同类型的XML回复字符串
    """
    # 微信的文档果然坑！！！ 为了严谨！文本内容模板使用的是官方样例，只替换了其中的变量。结果死活不行，最后想起来它应该是标准的XML格式，仔细查看内容发现了< !之间及] ] 之间多余的空格。消除后立即解决！浪费我3天！！！
    def parse_msg_event(self, xml=None, *args, **kwargs):
        # xml为XML格式的字符串，返回字典格式解析结果
        result = {}
        try:
            tree = ET.fromstring(xml)
            result['from_user'] = tree.find('FromUserName').text
            result['to_user'] = tree.find('ToUserName').text
            result['create_time'] = tree.find('CreateTime').text
            result['msg_type'] = tree.find('MsgType').text
            if tree.find('MsgId') is not None:
                result['msg_id'] = tree.find('MsgId').text
            if result['msg_type'] == 'text':
                result['content'] = tree.find('Content').text
            elif result['msg_type'] == 'image':
                result['msg_id'] = tree.find('MsgId').text
                result['pic_url'] = tree.find('PicUrl').text
                result['media_id'] = tree.find('MediaId').text
            elif result['msg_type'] == 'voice':
                result['media_id'] = tree.find('MediaId').text
                result['format'] = tree.find('Format').text
                result['recognition'] = tree.find('recognition').text
            elif result['msg_type'] == 'video':
                result['media_id'] = tree.find('MediaId').text
                result['thumb_media_id'] = tree.find('ThumbMediaId').text
            elif result['msg_type'] == 'shortvideo':
                result['media_id'] = tree.find('MediaId').text
                result['thumb_media_id'] = tree.find('ThumbMediaId').text
            elif result['msg_type'] == 'location':
                result['location_x'] = tree.find('Location_X').text
                result['location_y'] = tree.find('Location_Y').text
                result['scale'] = tree.find('Scale').text
                result['label'] = tree.find('Label').text
            elif result['msg_type'] == 'link':
                result['title'] = tree.find('Title').text
                result['description'] = tree.find('Description').text
                result['url'] = tree.find('Url').text
            elif result['msg_type'] == 'event':
                if tree.find('Event') is not None:
                    result['event'] = tree.find('Event').text
                if tree.find('EventKey') is not None:
                    result['event_key'] = tree.find('EventKey').text
                if tree.find('Ticket') is not None:
                    result['ticket'] = tree.find('Ticket').text
                if tree.find('Latitude') is not None:
                    result['latitude'] = tree.find('Latitude').text
                if tree.find('Longitude') is not None:
                    result['longitude'] = tree.find('Longitude').text
            return result
        except Exception as e:
            print(e)
            raise e

    def get_text_msg(self, msg_paras, *args, **kwargs):
        """
        msg_paras里必须包含to_user, from_user, content三个值
        返回XML字符串
        """
        template = """<xml>
                <ToUserName><![CDATA[{to_user}]]></ToUserName>
                <FromUserName><![CDATA[{from_user}]]></FromUserName>
                <CreateTime>{create_time}</CreateTime>
                <MsgType><![CDATA[text]]></MsgType>
                <Content><![CDATA[{content}]]></Content>
                </xml>""".format(**msg_paras)
        return template

    def get_image_msg(self, msg_paras, *args, **kwargs):
        """
        msg_paras里必须包含to_user, from_user, media_id三个值
        返回XML字符串
        """
        template = """<xml>
                <ToUserName><![CDATA[{to_user}]]></ToUserName>
                <FromUserName><![CDATA[{from_user}]]></FromUserName>
                <CreateTime>{create_time}</CreateTime>
                <MsgType><![CDATA[image]]></MsgType>
                <Image>
                    <MediaId><![CDATA[{media_id}]]></MediaId>
                </Image>
                </xml>""".format(**msg_paras)
        return template

    def get_voice_msg(self, msg_paras, *args, **kwargs):
        """
        msg_paras里必须包含to_user, from_user, media_id三个值
        返回XML字符串
        """
        template = """<xml>
                <ToUserName><![CDATA[{to_user}]]></ToUserName>
                <FromUserName><![CDATA[{from_user}]]></FromUserName>
                <CreateTime>{create_time}</CreateTime>
                <MsgType><![CDATA[voice]]></MsgType>
                <Voice>
                    <MediaId><![CDATA[{media_id}]]></MediaId>
                </Voice>
                </xml>""".format(**msg_paras)
        return template

    def get_video_msg(self, msg_paras, *args, **kwargs):
        """
        msg_paras里必须包含to_user, from_user, media_id, title, description五个值
        后两个参数可为空字符串
        返回XML字符串
        """
        template = """<xml>
                <ToUserName><![CDATA[{to_user}]]></ToUserName>
                <FromUserName><![CDATA[{from_user}]]></FromUserName>
                <CreateTime>{create_time}</CreateTime>
                <MsgType><![CDATA[video]]></MsgType>
                <Video>
                    <MediaId><![CDATA[{media_id}]]></MediaId>
                    <Title><![CDATA[title]]</Title>
                    <Description><![CDATA[description]]</Description>
                </Video>
                </xml>""".format(**msg_paras)
        return template

    def get_music_msg(self, msg_paras, *args, **kwargs):
        """
        msg_paras里必须包含to_user, from_user, media_id, title, description五个值
        后两个参数可为空字符串
        返回XML字符串
        """
        template = """<xml>
                <ToUserName><![CDATA[{to_user}]]></ToUserName>
                <FromUserName><![CDATA[{from_user}]]></FromUserName>
                <CreateTime>{create_time}</CreateTime>
                <MsgType><![CDATA[music]]></MsgType>
                <Music>
                    <Title><![CDATA[title]]</Title>
                    <Description><![CDATA[description]]</Description>
                    <MusicUrl><![CDATA[{music_url}]]></MusicUrl>
                    <HQMusicUrl><![CDATA[{hq_music_url}]]></HQMusicUrl>
                    <ThumbMediaId><![CDATA[{media_id}]]></ThumbMediaId>
                </Music>
                </xml>""".format(**msg_paras)
        return template

    def get_news_msg(self, msg_paras, *args, **kwargs):
        """
        msg_paras里必须包含to_user, from_user, media_id, title, description, pic_url, url七个值
        返回XML字符串
        """
        template = """<xml>
                <ToUserName><![CDATA[{to_user}]]></ToUserName>
                <FromUserName><![CDATA[{from_user}]]></FromUserName>
                <CreateTime>{create_time}</CreateTime>
                <MsgType><![CDATA[news]]></MsgType>
                <ArticleCount>1</ArticleCount>
                <Articles>
                  <item>
                    <Title><![CDATA[title]]</Title>
                    <Description><![CDATA[description]]</Description>
                    <PicUrl><![CDATA[{picture_url}]]></PicUrl>
                    <Url><![CDATA[{url}]]></Url>
                  </item>
                </Articles>
                </xml>""".format(**msg_paras)
        return template


class MenuAPI(object):
    """
    微信公众号菜单管理
    """
    def __init__(self, access_token=None, *args, **kwargs):
        if access_token is None:
            raise InvalidTokenException('Invalid access token')
        self.access_token = access_token

    def create_menu(self, json_data=None, *args, **kwargs):
        """
        创建微信公众号菜单
        """
        url = 'https://api.weixin.qq.com/cgi-bin/menu/create?access_token={}'.format(self.access_token)
        # print(url)
        if json_data is None:
            # 无参数时用默认菜单
            button1 = {'type':'view', 'name':'微官网', 'url':'http://123.56.115.20:8080/#/home'}
            button2_sub1 = {'type':'view', 'name':'我的订单', 'url': 'http://123.56.115.20:8080/#/my_order'}
            button2_sub2 = {'type':'view', 'name':'我的礼券', 'url': 'http://123.56.115.20:8080/#/my_coupon'}
            button2_sub3 = {'type':'view', 'name':'我的优享', 'url': 'http://123.56.115.20:8080/#/my_info'}
            button2 = {'name': '个人专区', 'sub_button': [button2_sub1,button2_sub2,button2_sub3]}
            button3_sub1 = {'type':'view', 'name':'你', 'url': 'http://123.56.115.20:8080/#/home'}
            button3_sub2 = {'type':'view', 'name':'他', 'url': 'http://123.56.115.20:8080/#/shop'}
            button3_sub3 = {'type':'click', 'name':'赞', 'key': 'good'}
            button3 = {'name': '分享有礼', 'sub_button': [button3_sub1,button3_sub2,button3_sub3]}
            buttons = {'button':[button1,button2,button3]}
            json_data = json.dumps(buttons, ensure_ascii=False)
        try:
            r = requests.post(url, json_data.encode('utf-8'))
            return r
        except Exception as e:
            print(e)
            raise e

    def get_menu(self, *args, **kwargs):
        """
        查询微信公众号菜单
        """
        url = 'https://api.weixin.qq.com/cgi-bin/menu/get?access_token={}'.format(self.access_token)
        # print(url)
        r = requests.get(url)
        return r

    def delete_menu(self, *args, **kwargs):
        """
        删除微信公众号菜单
        """
        url = 'https://api.weixin.qq.com/cgi-bin/menu/delete?access_token={}'.format(self.access_token)
        # print(url)
        r = requests.get(url)
        return r

    def create_conditional_menu(self, json_data=None, *args, **kwargs):
        """
        创建微信公众号个性化菜单
        """
        url = 'https://api.weixin.qq.com/cgi-bin/menu/addconditional?access_token={}'.format(self.access_token)
        # print(url)
        if json_data is None:
            # 无参数时用默认菜单
            button1 = {'type':'click', 'name':'我', 'key':'me'}
            button2_sub1 = {'type':'view', 'name':'你', 'url': 'http://123.56.115.20:8000'}
            button2_sub2 = {'type':'view', 'name':'他', 'url': 'http://123.56.115.20:8000'}
            button2_sub3 = {'type':'click', 'name':'赞', 'key': 'good'}
            button2 = {'name': '菜单', 'sub_button': [button2_sub1,button2_sub2,button2_sub3]}
            button3 = {'name': '菜单', 'sub_button': [button2_sub1,button2_sub2,button2_sub3]}
            matchrule = {'sex': '1', 'client_platform_type':'1'}
            buttons = {'button':[button1,button2,button3], 'matchrule':matchrule}
            json_data = json.dumps(buttons, ensure_ascii=False)
        r = requests.post(url, json_data.encode('utf-8'))
        return r

    def delete_conditional_menu(self, menuid=None, *args, **kwargs):
        """
        删除微信公众号个性化菜单
        """
        url = 'https://api.weixin.qq.com/cgi-bin/menu/delconditional?access_token={}'.format(self.access_token)
        # print(url)
        if menuid is None:
            # 无参数时用默认菜单
            raise ValueError('Invalid menuid')
        json_data = """{"menuid":"{}"}""".format(menuid)
        r = requests.post(url, json_data.encode('utf-8'))
        return r

    def try_conditional_menu(self, user_id=None, *args, **kwargs):
        """
        测试微信公众号个性化菜单
        """
        url = 'https://api.weixin.qq.com/cgi-bin/menu/trymatch?access_token={}'.format(self.access_token)
        # print(url)
        if user_id is None:
            # 无参数时用默认菜单
            raise ValueError('Invalid user_id')
        json_data = """{"user_id":"{}"}""".format(user_id)
        r = requests.post(url, json_data.encode('utf-8'))
        return r

    def get_current_selfmenu(self, *args, **kwargs):
        """
        获取当前自定义菜单
        """
        url = 'https://api.weixin.qq.com/cgi-bin/get_current_selfmenu_info?access_token={}'.format(self.access_token)
        # print(url)
        r = requests.get(url)
        return r


class MessageAPI(object):
    """
    微信公众号消息管理
    """
    def __init__(self, access_token=None, *args, **kwargs):
        if access_token is None:
            raise InvalidTokenException('Invalid access token: ', access_token)
        self.access_token = access_token

    def get_current_autoreplay_info(self, *args, **kwargs):
        """
        查询微信公众号当前自动回复内容
        """
        url = 'https://api.weixin.qq.com/cgi-bin/get_current_autoreply_info?access_token={}'.format(self.access_token)
        r = requests.get(url)
        return r

    def get_weixin_server_ip(self, *args, **kwargs):
        """
        获取微信服务器IP，返回字典类型结果
        """
        url = 'https://api.weixin.qq.com/cgi-bin/getcallbackip?access_token={}'.format(self.access_token)
        # print(url)
        r = requests.get(url)
        json_data = json.loads(r.content.decode(), ensure_ascii=False)
        return json_data


class MaterialAPI(object):
    """
    微信公众号素材管理
    """
    def __init__(self, access_token=None, *args, **kwargs):
        if access_token is None:
            raise InvalidTokenException('Invalid access token')
        self.access_token = access_token

    def upload_tmp_material(self, m_type='image', medias=None, *args, **kwargs):
        """
        上传临时素材
        """
        url = 'https://api.weixin.qq.com/cgi-bin/media/upload?access_token={token}&type={m_type}'.format(token=self.access_token, m_type=m_type)
        medias = {
            'media': ('m1', open(filepath, 'rb'), 'image/jpeg')
        }
        r = requests.post(url, files=medias)
        return r

    def get_tmp_material(self, media_id=None, *args, **kwargs):
        """
        获取临时素材
        """
        url = 'https://api.weixin.qq.com/cgi-bin/media/get?access_token={token}&media_id={media_id}'.format(token=self.access_token, media_id=media_id)
        r = requests.post(url)
        return r

    def upload_news(self, json_data=None,  *args, **kwargs):
        """
        上传图文类素材
        """
        url = 'https://api.weixin.qq.com/cgi-bin/material/add_news?access_token={token}'.format(token=self.access_token)
        格式样例
        # json_data = {
        #     "articles": [{
        #     "title": TITLE,
        #     "thumb_media_id": THUMB_MEDIA_ID,
        #     "author": AUTHOR,
        #     "digest": DIGEST,
        #     "show_cover_pic": SHOW_COVER_PIC(0 / 1),
        #     "content": CONTENT,
        #     "content_source_url": CONTENT_SOURCE_URL
        #     },
        #     //若新增的是多图文素材，则此处应还有几段articles结构
        #     ]
        # }
        r = requests.post(url, json_data.encode('utf-8'))
        return r

    def update_news(self, json_data=None,  *args, **kwargs):
        """
        上传图文类素材
        """
        url = 'https://api.weixin.qq.com/cgi-bin/material/update_news?access_token={token}'.format(token=self.access_token)
        格式样例
        # json_data = {
        #     "articles": [{
        #     "title": TITLE,
        #     "thumb_media_id": THUMB_MEDIA_ID,
        #     "author": AUTHOR,
        #     "digest": DIGEST,
        #     "show_cover_pic": SHOW_COVER_PIC(0 / 1),
        #     "content": CONTENT,
        #     "content_source_url": CONTENT_SOURCE_URL
        #     },
        #     //若新增的是多图文素材，则此处应还有几段articles结构
        #     ]
        # }
        r = requests.post(url, json_data.encode('utf-8'))
        return r

    def get_material(self, media_id=None, *args, **kwargs):
        """
        获取素材
        """
        url = 'https://api.weixin.qq.com/cgi-bin/material/get_material?access_token={token}'.format(token=self.access_token)
        json_data = {
            'media_id': media_id
        }
        r = requests.post(url, json_data.encode('utf-8'))
        return r

    def del_material(self, media_id=None, *args, **kwargs):
        """
        删除素材
        """
        url = 'https://api.weixin.qq.com/cgi-bin/material/del_material?access_token={token}'.format(token=self.access_token)
        json_data = {
            'media_id': media_id
        }
        r = requests.post(url, json_data.encode('utf-8'))
        return r

    def upload_img(self, medias=None,  *args, **kwargs):
        """
        上传临时素材
        """
        url = 'https://api.weixin.qq.com/cgi-bin/media/uploadimg?access_token={token}'.format(token=self.access_token)
        # medias = {
        #     'media': ('m1', open(filepath, 'rb'), 'image/jpeg')
        # }
        r = requests.post(url, files=medias)
        return r

    def get_material_count(self, *args, **kwargs):
        """
        获取素材统计
        """
        url = 'https://api.weixin.qq.com/cgi-bin/material/get_materialcount?access_token={token}'.format(token=self.access_token)
        r = requests.post(url)
        return r

    def batch_get_material(self, m_type='image', offset=0, count=1, *args, **kwargs):
        """
        """
        url = 'https://api.weixin.qq.com/cgi-bin/material/batchget_material?access_token={}'.format(self.access_token)
        if json_data is None:
            # 无参数时用默认菜单
            data = {'type': m_type, 'offset': offset, 'count': count}
            json_data = json.dumps(data, ensure_ascii=False)
        r = requests.post(url, json_data.encode('utf-8'))
        return r


class UserAPI(object):
    """
    微信用户管理接口
    """
    def __init__(self, access_token=None, *args, **kwargs):
        if access_token is None:
            raise InvalidTokenException('Invalid access token')
        self.access_token = access_token

    def create_tag(self, json_data=None,  *args, **kwargs):
        """
        json_data = { 'tag': { 'name': 'tag_name' // 标签名 }}
        """
        url = """https://api.weixin.qq.com/cgi-bin/tags/create?access_token={}""".format(self.access_token)
        try:
            r = requests.post(url, json_data.encode('utf-8'))
            return r
        except Exception as e:
            print(e)
            raise e

    def get_tags(self, *args, **kwargs):
        """
        """
        url = """https://api.weixin.qq.com/cgi-bin/tags/get?access_token={}""".format(self.access_token)
        try:
            r = requests.post(url)
            return r
        except Exception as e:
            print(e)
            raise e

    def update_tag(self, json_data=None,  *args, **kwargs):
        """
        json_data = { 'tag': { 'id': 123,  'name': 'tag_name' // 标签名 }}
        """
        url = """https://api.weixin.qq.com/cgi-bin/tags/update?access_token={}""".format(self.access_token)
        try:
            r = requests.post(url, json_data.encode('utf-8'))
            return r
        except Exception as e:
            print(e)
            raise e

    def delete_tag(self, json_data=None,  *args, **kwargs):
        """
        json_data = { 'tag': { 'id': 123}}
        """
        url = """https://api.weixin.qq.com/cgi-bin/tags/delete?access_token={}""".format(self.access_token)
        try:
            r = requests.post(url, json_data.encode('utf-8'))
            return r
        except Exception as e:
            print(e)
            raise e

    def get_tag_users(self, json_data=None,  *args, **kwargs):
        """
        json_data = { 'tagid': 123, 'next_openid': ""}
        """
        url = """https://api.weixin.qq.com/cgi-bin/user/tag/get?access_token={}""".format(self.access_token)
        try:
            r = requests.post(url, json_data.encode('utf-8'))
            return r
        except Exception as e:
            print(e)
            raise e

    def batch_tag_users(self, json_data=None,  *args, **kwargs):
        """
        json_data = { 'openid_list': [], 'tagid': 123}
        """
        url = """https://api.weixin.qq.com/cgi-bin/tags/members/batchtagging?access_token={}""".format(self.access_token)
        try:
            r = requests.post(url, json_data.encode('utf-8'))
            return r
        except Exception as e:
            print(e)
            raise e

    def batch_untag_users(self, json_data=None,  *args, **kwargs):
        """
        json_data = { 'openid_list': [], 'tagid': 123}
        """
        url = """https://api.weixin.qq.com/cgi-bin/tags/members/batchuntagging?access_token={}""".format(self.access_token)
        try:
            r = requests.post(url, json_data.encode('utf-8'))
            return r
        except Exception as e:
            print(e)
            raise e

    def get_user_tags(self, json_data=None,  *args, **kwargs):
        """
        json_data = { 'openid': ""}
        """
        url = """https://api.weixin.qq.com/cgi-bin/tags/getidlist?access_token={}""".format(self.access_token)
        try:
            r = requests.post(url, json_data.encode('utf-8'))
            return r
        except Exception as e:
            print(e)
            raise e

    def set_user_remark(self, json_data=None,  *args, **kwargs):
        """
        json_data = { 'openid': 'asdflasjdf', 'remark': 'beauty' }
        """
        url = """https://api.weixin.qq.com/cgi-bin/user/info/updateremark?access_token={}""".format(self.access_token)
        try:
            r = requests.post(url, json_data.encode('utf-8'))
            return r
        except Exception as e:
            print(e)
            raise e

    def get_user_info(self, openid=None, lang='zh_CN', *args, **kwargs):
        """
        """
        url = """https://api.weixin.qq.com/cgi-bin/user/info?access_token={token}&openid={openid}&lang={lang}""".format(token=self.access_token, openid=openid, lang=lang)
        try:
            r = requests.get(url)
            return r
        except Exception as e:
            print(e)
            raise e

    def batchget_user_info(self, json_data=None,  *args, **kwargs):
        """
        json_data = { 'user_list': [{'openid':asldfj', 'lang': 'zh_CN'}, {}]}
        """
        url = """https://api.weixin.qq.com/cgi-bin/user/info/batchget?access_token={token}""".format(token=self.access_token)
        try:
            r = requests.post(url, json_data.encode('utf-8'))
            return r
        except Exception as e:
            print(e)
            raise e

    def get_user_list(self, next_openid=None, *args, **kwargs):
        """
        """
        if next_openid is None:
            url = """https://api.weixin.qq.com/cgi-bin/user/get?access_token={token}""".format(token=self.access_token)
        else:
            url = """https://api.weixin.qq.com/cgi-bin/user/get?access_token={token}&next_openid={next_openid}""".format(token=self.access_token, next_openid=next_openid)
        try:
            r = requests.get(url)
            return r
        except Exception as e:
            print(e)
            raise e

    def get_blacklist(self, json_data=None,  *args, **kwargs):
        """
        json_data = { 'begin_openid': 'openid' }
        """
        url = """https://api.weixin.qq.com/cgi-bin/tags/members/getblacklist?access_token={token}""".format(token=self.access_token)
        try:
            r = requests.post(url, json_data.encode('utf-8'))
            return r
        except Exception as e:
            print(e)
            raise e

    def batch_blacklist(self, json_data=None,  *args, **kwargs):
        """
        json_data = { 'openid_list': ['openid1', 'openid2'...] }
        """
        url = """https://api.weixin.qq.com/cgi-bin/tags/members/batchblacklist?access_token={token}""".format(token=self.access_token)
        try:
            r = requests.post(url, json_data.encode('utf-8'))
            return r
        except Exception as e:
            print(e)
            raise e

    def batch_unblacklist(self, json_data=None,  *args, **kwargs):
        """
        json_data = { 'openid_list': ['openid1', 'openid2'...] }
        """
        url = """https://api.weixin.qq.com/cgi-bin/tags/members/batchunblacklist?access_token={token}""".format(token=self.access_token)
        try:
            r = requests.post(url, json_data.encode('utf-8'))
            return r
        except Exception as e:
            print(e)
            raise e


class MerchantAPI(object):
    """
    微信门店商品管理接口
    待写
    """
    def __init__(self, access_token=None, *args, **kwargs):
        if access_token is None:
            raise InvalidTokenException('Invalid access token')
        self.access_token = access_token

    def create_merchant(self, json_data=None, *args, **kwargs):
        """
        """
        url = """https://api.weixin.qq.com/merchant/create?access_token={}""".format(self.access_token)
        try:
            r = requests.post(url, json_data.encode('utf-8'))
            return r
        except Exception as e:
            print(e)
            raise e

    def delete_merchant(self, json_data=None, *args, **kwargs):
        """
        json_data = { "product_id": "alsdkfjasldfjs" }
        """
        url = """https://api.weixin.qq.com/merchant/del?access_token={}""".format(self.access_token)
        try:
            r = requests.post(url, json_data.encode('utf-8'))
            return r
        except Exception as e:
            print(e)
            raise e

    def update_merchant(self, json_data=None, *args, **kwargs):
        """
        """
        url = """https://api.weixin.qq.com/merchant/update?access_token={}""".format(self.access_token)
        try:
            r = requests.post(url, json_data.encode('utf-8'))
            return r
        except Exception as e:
            print(e)
            raise e

    def get_merchant(self, json_data=None, *args, **kwargs):
        """
        """
        url = """https://api.weixin.qq.com/merchant/get?access_token={}""".format(self.access_token)
        if json_data is None:
            try:
                r = requests.get(url)
                return r
            except Exception as e:
                print(e)
                raise e
        else:
            try:
                r = requests.post(url, json_data.encode('utf-8'))
                return r
            except Exception as e:
                print(e)
                raise e

    def get_merchant_by_status(self, json_data=None, *args, **kwargs):
        """
        """
        url = """https://api.weixin.qq.com/merchant/getbystatus?access_token={}""".format(self.access_token)
        try:
            r = requests.post(url, json_data.encode('utf-8'))
            return r
        except Exception as e:
            print(e)
            raise e

    def mod_product_status(self, json_data=None,  *args, **kwargs):
        """
        """
        url = """https://api.weixin.qq.com/merchant/modproductstatus?access_token={}""".format(self.access_token)
        try:
            r = requests.post(url, json_data.encode('utf-8'))
            return r
        except Exception as e:
            print(e)
            raise e

