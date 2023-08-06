from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client


# 腾讯云的cos操作工具类

class Cos(object):
    def __init__(self, cos_secret_id, cos_secret_key, region, bucket, domain):
        # 1. 设置用户属性, 包括 secret_id, secret_key, region 等。Appid 已在 CosConfig 中移除，请在参数 Bucket 中带上 Appid。Bucket 由 BucketName-Appid 组成
        secret_id = cos_secret_id  # 用户的 SecretId，建议使用子账号密钥，授权遵循最小权限指引，降低使用风险。子账号密钥获取可参见 https://cloud.tencent.com/document/product/598/37140
        secret_key = cos_secret_key  # 用户的 SecretKey，建议使用子账号密钥，授权遵循最小权限指引，降低使用风险。子账号密钥获取可参见 https://cloud.tencent.com/document/product/598/37140
        region = region  # 替换为用户的 region，已创建桶归属的 region 可以在控制台查看，https://console.cloud.tencent.com/cos5/bucket
        # COS 支持的所有 region 列表参见 https://cloud.tencent.com/document/product/436/6224
        token = None  # 如果使用永久密钥不需要填入 token，如果使用临时密钥需要填入，临时密钥生成和使用指引参见 https://cloud.tencent.com/document/product/436/14048
        scheme = 'https'  # 指定使用 http/https 协议来访问 COS，默认为 https，可不填

        config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
        self.client = CosS3Client(config)
        self.bucket = bucket
        self.domain = domain


    # 判断文件是否存在
    def exist(self, key):
        response = self.client.object_exists(
            Bucket=self.bucket,
            Key=key)
        # print(response)
        return response


    #### 文件流简单上传（不支持超过5G的文件，推荐使用下方高级上传接口）
    # 强烈建议您以二进制模式(binary mode)打开文件,否则可能会导致错误
    def upload_file_from_local_file(self, local_file_path, key):
        with open(local_file_path, 'rb') as fp:
            response = self.client.put_object(
                Bucket=self.bucket,
                Body=fp,
                Key=key,
                StorageClass='STANDARD',
                EnableMD5=False
            )
        # print(response['ETag'])
        url = self.domain + '/' + key
        return url

    #### 字节流简单上传
    def upload_file_from_bytes(self, data_bytes, key):
        response = self.client.put_object(
            Bucket=self.bucket,
            Body=data_bytes,
            Key=key,
            EnableMD5=False
        )
        # print(response['ETag'])
        url = self.domain + '/' + key
        return url

    # 网络流将以 Transfer-Encoding:chunked 的方式传输到 COS
    # import requests
    # stream = requests.get('https://cloud.tencent.com/document/product/436/7778')
    def upload_file_from_stream(self, stream, key):
        response = self.client.put_object(
            Bucket=self.bucket,
            Body=stream,
            Key=key,
            EnableMD5=False
        )
        # print(response['ETag'])
        url = self.domain + '/' + key
        return url

    def upload_file_from_url(self, url, key):
        import requests
        stream = requests.get(url)
        return self.upload_file_from_stream(stream, key)

    #### 高级上传接口（推荐）
    # 根据文件大小自动选择简单上传或分块上传，分块上传具备断点续传功能。
    def upload_file(self, local_file_path, key, part_size=1, max_thread=10, enable_md5=False):
        response = self.client.upload_file(
            Bucket=self.bucket,
            LocalFilePath=local_file_path,
            Key=key,
            PartSize=part_size,
            MAXThread=max_thread,
            EnableMD5=enable_md5
        )
        # print(response['ETag'])
        url = self.domain + '/' + key
        return url
