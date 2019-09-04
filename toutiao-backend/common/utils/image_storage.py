from flask import current_app
from qiniu import Auth, put_data


def upload_file(file_data):
    """
    七牛云上传

    :param file_data 上传的二进制数据
    :return: 文件名
    """
    #需要填写你的 Access Key 和 Secret Key
    access_key = current_app.config['QINIU_ACCESS_KEY']
    secret_key = current_app.config['QINIU_SECRET_KEY']
    #构建鉴权对象
    q = Auth(access_key, secret_key)

    # 要上传的空间
    bucket_name = current_app.config['QINIU_BUCKET_NAME']
    # 上传后保存的文件名  如果为None 自动生成文件名(hash值)
    key = None
    #生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, key, 3600 * 1000)

    ret, info = put_data(token, key, file_data)
    # 判断请求结果
    if info.status_code == 200:
        return ret.get('key')
    else:
        raise Exception(info.error)


if __name__ == '__main__':
    with open('123.jpg', 'rb') as f:
        img_bytes = f.read()
        file_name = upload_file(img_bytes)
        print(file_name)