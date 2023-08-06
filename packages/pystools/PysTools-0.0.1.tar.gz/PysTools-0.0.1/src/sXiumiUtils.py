# 绑定秀米账号
import hashlib
import json
import os
import random
import time

import urllib3

from utils.Config import get_tenant_config
from utils.Feishu3 import Feishu3
from utils.FeishuUtils import get_bot_info
from utils.HandleOss import HandleOSS
from utils.custom_log import append_custom_log_file

from src import Feishu

http = urllib3.PoolManager()

from sLogger import logger


class XiumiUtils(object):
    def __init__(self, tenant_code):
        self.tenant_code = tenant_code
        self.xiumi_conf = get_tenant_config('xiumi', tenant_code)
        self.appid = self.xiumi_conf.get('app_id')
        self.secret = self.xiumi_conf.get('app_secret')
        self.feishu = Feishu3(tenant_code=tenant_code)

    def partner_bind(self, partner_user_id):
        """
        绑定秀米账号
        https://ent.xiumi.us/doc2.html
        :param partner_user_id:  用户在平台（不是秀米）的唯一ID。 可以不使用平台的用户编号，而为秀米对接特地生成一个专用的ID字符串。建议是飞书的user ID
        :return:
        """
        timestamp = int(time.time())  # 1544426764   当前UNIX时间戳，单位：秒。需不早于当前时间5分钟。
        nonce = random.randint(100000, 999999)  # 随机字符串，由您的平台在每一次签名时生成，使用于签名算法内。如 590946
        partner_user_id = partner_user_id  # 用户在平台（不是秀米）的唯一ID。 可以不使用平台的用户编号，而为秀米对接特地生成一个专用的ID字符串。
        data = [str(partner_user_id), str(self.secret), str(timestamp), str(nonce)]
        data.sort()
        cs = "".join(data)
        signature = hashlib.md5(cs.encode(encoding='UTF-8')).hexdigest()
        signature = hashlib.md5(signature.encode(encoding='UTF-8')).hexdigest()
        url = "https://xiumi.us/auth/partner/bind?signature={}&timestamp={}&nonce={}&partner_user_id={}&appid={}".format(
            signature, timestamp, nonce, partner_user_id, self.appid
        )
        return url

    def upload_file(self, file_name, file_data):
        file_dir = self.xiumi_conf.get('default_file_dir')
        oss_path = "{}/{}".format(file_dir, file_name)
        OSS_handle = HandleOSS(tenant_code=self.tenant_code)
        img_url = OSS_handle.update_data(file_data, oss_path)
        return img_url

    def update_article_record(self, artitle, json_url,partner_user_id):
        aid = artitle.get("article_id", 0)
        title = artitle.get("title", "")
        picurl = artitle.get("picurl", "")
        summary = artitle.get("summary", "")
        description = artitle.get("description", "")
        tags = artitle.get("tags", [])
        url = artitle.get("url", [])

        app_token = self.xiumi_conf.get('default_feishu_bitable_app_token')
        # 上传图片到飞书
        file_name = "xiumi_artticle_{}_{}".format(aid, os.path.basename(picurl))
        res = http.request("GET", picurl)
        file_bytes = res.data
        feishu_file = self.feishu.upload_file(app_token, file_name, file_bytes, "bitable_image")

        table_id = self.xiumi_conf.get('default_feishu_bitable_table_id')
        record_id = None
        res = self.feishu.bitable_records(app_token, table_id
                                          , {
                                              'filter': 'CurrentValue.[(A)秀米文章ID]={}'.format(aid)
                                          })
        aitems = res.get("items", [])
        if aitems:
            record_id = aitems[0].get("record_id", None)
        cmdstr = "待审核"
        xm_url = {'link': 'https://c.xiumi.us/board/v5/5yLHh/{}'.format(aid), 'text': '{}'.format(title)}
        artitle_url = {'link': json_url, 'text': '{}.json'.format(aid)}

        data = {
            "fields": {
                "(C)标题": title,
                "(C)副标题": summary,
                "(A)内容": description,
                "(A)秀米文章ID": aid,
                "(A)秀米文章链接": xm_url,
                "(A文章内容": artitle_url,
                "(C)封面图片": [feishu_file],
                "(C)上传指令": cmdstr,
            }
        }

        user_info = self.feishu.get_contact_users(partner_user_id, {"user_id_type": 'user_id'})
        if user_info.get('user',None):
            user_open_id = user_info.get('user').get('open_id',None)
            if user_open_id:
                data['fields']['(A)内容编辑人'] = [{"id": user_open_id}]

        self.logger.info('更新文章内容数据表app_token: {}  table_id: {}  record_id:{} '.format(app_token, table_id, record_id))
        res1 = self.feishu.bitable_records(app_token, table_id, record_id=record_id, req_body=data)
        return res1

    def feishu_bot_bind_user(self, message,sender,feishu: Feishu):
        # print('+++++++++++++', message)

        bot_openid = feishu.bot_info().get('open_id')

        sender_id = sender.get("sender_id", {})
        user_id = sender_id.get("user_id", str(random.randint(100000, 999999)))
        # message = event.get("message", {})
        message_type = message.get("message_type", "")
        chat_type = message.get("chat_type", "")
        chat_id = message.get("chat_id", "")
        mentions = message.get("mentions", [])
        msg_text = ''
        if "text" in message_type:
            content = message.get("content", "")
            content_json = json.loads(content)
            msg_text = content_json.get("text", "")

        # 如果收到 绑定秀米 就回复绑定链接
        msg_type = "text"
        receive_id_type = ""
        receive_id = ""
        is_mention_bot = False
        bot_name = '机器人'
        if "p2p" in chat_type:
            receive_id_type = "user_id"
            receive_id = user_id
        elif "group" in chat_type:
            receive_id_type = "chat_id"
            receive_id = chat_id
            if mentions:
                mention_openids = []
                for mention in mentions:
                    ids = mention.get("id", {})
                    # print('================',mention)

                    bot_name = mention.get("name", '机器人')
                    mention_openids.append(ids.get("open_id"))
                # 如果提到了机器人
                if bot_openid in mention_openids:
                    is_mention_bot = True
        # print('================bot_openid', bot_openid)
        # print('================is_mention_bot', is_mention_bot)
        # print('================msg_text', msg_text)
        send_cmd = False
        bind_url = self.partner_bind(user_id)
        text = "您的专属绑定链接已生成，请在【五分钟内】使用，过期失效\n" \
               "1、请先在默认浏览器中登录您的秀米账号\n" \
               "2、点击以下链接，确认在登录秀米账号的浏览器中打开\n" \
               "{} \n\n 如需解绑，请回复【解绑秀米账号】并@{}".format(bind_url,bot_name)
        if "解绑秀米" in msg_text:
            text = "1、请先在默认浏览器中登录您的秀米账号\n" \
                   "2、点击以下链接，确认在登录秀米账号的浏览器中打开\n" \
                   "3、点击链接，进入解绑页面 https://xiumi.us/#/user/partnerbind " \
                   "\n\n 如需绑带秀米账号，请回复【绑定秀米账号】并@{}".format(bot_name)
            if "p2p" in chat_type:
                send_cmd = True
            elif is_mention_bot:
                send_cmd = True
                text = "<at user_id=\"{}\">Tom</at> {}".format(user_id, text)

        if "绑定秀米" in msg_text:
            if "p2p" in chat_type:
                send_cmd = True
            elif is_mention_bot:
                send_cmd = True
                text = "<at user_id=\"{}\">Tom</at> {}".format(user_id, text)

        content = json.dumps({"text": text}, ensure_ascii=False)
        resp_data = {
            'to_send': send_cmd,
            "receive_id_type": receive_id_type,
            "receive_id": receive_id,
            "msg_type": msg_type,
            "content": content
        }

        return resp_data


if __name__ == '__main__':
    appid = "c29c081d41a0e2f839a7ded2364e5566"
    secret = "c2656450694f5ec054b4ca8b5f93ff5b"
    exec = XiumiUtils(appid, secret)
    print(exec.partner_bind("123"))
