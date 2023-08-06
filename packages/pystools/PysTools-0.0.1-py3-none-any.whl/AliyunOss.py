# -*- coding: utf-8 -*-
import datetime
import oss2
import os

import urllib3

from sLogger import logger

HTTP_POOL = urllib3.PoolManager(num_pools=1000)


class HandleOSS(object):
    def __init__(self, key_id='', key_secret='', endpoint='', bucket_name='', domian='',
                 log_conf={}):
        '''
        初始化
        :param key_id:
        :param key_secret:
        :param bucket: bucket名称, 这里是qmgy-private-hz-dev
        '''

        if not key_id or not key_secret or not endpoint or not bucket_name or not domian:
            raise Exception('appid、 secret 、 endpoint、bucket_name、domian不能为空')
        self.logger = logger(**log_conf)
        self.key_id = key_id
        self.key_secret = key_secret
        self.endpoint = endpoint
        self.bucket_name = bucket_name
        self.domian = domian
        self.auth = oss2.Auth(self.key_id, self.key_secret)

        self.bucket = oss2.Bucket(self.auth, self.endpoint, self.bucket_name)

    def update_one_file(self, file_path, oss_path, backup=False) -> str:
        '''
        将文件上传到oss上
        :param file_dir: 要上传的文件
        :param oss_dir: oss上的路径, 要存在oss上的那个文件
        :param backup: 如果文件已存在，是否备份原来的文件，备份文件名为{name}_bck_20220917172359
        :return:
        '''

        file_name = file_path.split('/')[-1]
        # print("file_path===: ", file_path)
        self.logger.info("file_path===: {}".format(file_path))
        oss_save_path = f'{oss_path}/{file_name}'
        # print("oss_save_paht===: ", oss_save_path)
        self.logger.info("oss_save_paht===: {}".format(oss_save_path))

        if backup:
            if self.bucket.object_exists(oss_save_path):
                bak_name = oss_save_path + "_bak_" + datetime.datetime.now().strftime('%Y%m%d%H%M%S')
                self.bucket.copy_object(self.bucket.bucket_name, oss_save_path, bak_name)
                # print("备份文件",bak_name,self.domian + "/" +bak_name)
                self.logger.info("备份文件 {}/{}".format(self.domian, bak_name))
        # 上传
        res = self.bucket.put_object_from_file(oss_save_path, file_path)
        # print(res.status)
        # print(res.data)
        path = self.domian + "/" + oss_save_path
        self.logger.info("oss文件存储路径： {}".format(path))
        return path

    def update_data(self, data, oss_save_path, headers=None, backup=False) -> str:
        '''
        将文件上传到oss上
        :param data: 待上传的内容。
        :type data: bytes，str或file-like object

        :param oss_save_path: oss上的文件路径, 要存在oss上的那个文件夹，如： test/img.png

        :param headers: 用户指定的HTTP头部。可以指定Content-Type、Content-MD5、x-oss-meta-开头的头部等
        :type headers: 可以是dict，建议是oss2.CaseInsensitiveDict

        :param backup: 如果文件已存在，是否备份原来的文件，备份文件名为{name}_bck_20220917172359
        :return:
        '''
        # oss_save_path = f'{oss_path}/{file_name}'
        # print("oss_save_paht===: ", oss_save_path)

        if oss_save_path.startswith('/'):
            oss_save_path = oss_save_path[1:]

        if backup:
            if self.bucket.object_exists(oss_save_path):
                bak_name = oss_save_path + "_bak_" + datetime.datetime.now().strftime('%Y%m%d%H%M%S')
                self.bucket.copy_object(self.bucket_name, oss_save_path, bak_name)
                # print("备份文件", bak_name, self.domian + "/" + bak_name)
                self.logger.info("备份文件 {}/{}".format(self.domian, bak_name))

        res = self.bucket.put_object(oss_save_path, data, headers)
        # print("oss上传结果：", res)
        # print(res.data)
        path = self.domian + "/" + oss_save_path
        # print('oss文件存储路径：', path)
        self.logger.info("oss文件存储路径： {}".format(path))
        return path

    def update_data_from_url(self, url, oss_save_path, headers=None, backup=False) -> str:

        resp = HTTP_POOL.request(method="GET", url=url)
        resp_data = resp.data
        resp_header = resp.info()
        content_type = resp_header.get('Content-Type')
        Content_Disposition = resp_header.get('Content-Disposition')
        # print()
        return self.update_data(resp_data, oss_save_path, headers={'Content-Type': content_type})

    # 判断文件在不在
    def oss_file_exist(self, oss_file_path) -> dict:
        return self.bucket.object_exists(oss_file_path)

    def download_one_file(self, oss_path, save_dir):
        '''
        下载单个文件
        :param oss_path: 文件所在的oss地址
        :param save_dir: 要保存在本地的文件目录
        :return:
        '''

        file_name = oss_path.split('/')[-1]
        save_path = os.path.join(save_dir, file_name)
        # print("save_path===:", save_path)
        self.logger.info("save_path===: {}".format(save_path))
        result = self.bucket.get_object_to_file(oss_path, save_path)
        if result.status == 200:
            return '下载成功'
        pass

    def download_many_file(self, oss_dir, save_dir):
        '''
        批量下载文件
        :param oss_dir: oss上要下载的文件目录
        :param save_dir: 要存在本地的文件目录
        :return:
        '''

        obj = oss2.ObjectIterator(self.bucket, prefix=oss_dir)
        # 遍历oss文件夹获取所有的对象列表，i.key是文件的完整路径
        for i in obj:
            # 如果文件是以斜杠结尾的，说明不是文件，则跳过
            if i.key.endswith('/'):
                continue
            # 文件名：文件路径按照斜杠分割取最后一个
            file_name = i.key.split('/')[-1]
            # 下载到的具体路径
            save_path = os.path.join(save_dir, file_name)
            # 从oss下载
            self.bucket.get_object_to_file(i.key, save_path)


if __name__ == '__main__':
    file_path = "../apis/tools/oscilloscopes.json"
    download_oss_path = "feishu_files/oscilloscopes.json"
    save_dir = "../apis/tools"

    # oss配置
    oss_path = "feishu_files"
    oss_config = {
        "oss_domian": "https://resource.value-instrument.com",
        "endpoint": "http://oss-cn-beijing.aliyuncs.com",
        "accesskey_id": "LTAI5tQ95DrMRLLYZLRdKuVf",
        "accesskey_secret": "75pr556DYISgOSLog88T8c6NWlRdFJ",
        "bucket": "vi-public"
    }

    handle = HandleOSS(oss_config["accesskey_id"], oss_config["accesskey_secret"], oss_config["endpoint"],
                       oss_config["bucket"], oss_config["oss_domian"])
    handle.logger.info("oss_config===: {}".format(oss_config))
    res = handle.update_one_file(file_path, oss_path)
    print("上传成功:", res)
    # handle.download_one_file(download_oss_path, save_dir)
    # print('目录下载开始')
    # handle.download_many_file(oss_path, save_dir)
