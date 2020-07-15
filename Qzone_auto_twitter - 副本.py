import re
import time
from random import random

import requests


# Hash33算法
def hash33(t, e=0):
    for i in range(len(t)):
        e += (e << 5) + ord(t[i])
    return 2147483647 & e


# 用于登陆获取Cookie
def login():
    ss = requests.session()
    url = 'https://ssl.ptlogin2.qq.com/ptqrshow?appid=549000912&e=2&l=M&s=3&d=72&v=4&t=' + str(
        '0.' + str(int(random() * 10000000000000000)))
    response = ss.get(url=url)
    with open('qrcode.png', 'wb') as f:
        f.write(response.content)
    cookie = response.cookies
    headers = requests.utils.dict_from_cookiejar(cookie)
    print(headers)
    while True:
        url = f'https://ssl.ptlogin2.qq.com/ptqrlogin?u1=https%3A%2F%2Fqzs.qzone.qq.com%2Fqzone%2Fv5%2Floginsucc.Html' \
              f'%3Fpara%3Dizone%26from%3Diqq&ptqr' \
              f'token={hash33(headers["qrsig"])}&ptredirect=0&h=1&t=1&g=1&from_ui=1&ptlang=2052&action=0-0' \
              f'-1542784335061&js_ver=10289&js_type=1&login_sig=hn6ZiMZRPT8LWFsFG3MrScznzLVrdbwS9EIo-ihAmeD' \
              f'*YmOfqP3uoI6JytVVQYw2&pt_uistyle=40&aid=549000912&daid=5& '
        html = ss.get(url=url, headers=headers)
        type = re.findall('[\u4e00-\u9fa5]+', html.text)[0]
        if type == '二维码未失效':
            print(type)
        elif type == '二维码认证中':
            print(type)
        elif type == '登录成功':
            print(type)
            return html.cookies
        else:
            print("二维码已失效，请重新扫码！")
            login()
        time.sleep(2)


# 主体，用来发送说说的
def send():
    headers = {
        'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'origin': 'https://user.qzone.qq.com',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ApplewebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/83.0.4103.61 Safari/537.36',
    }
    cookie = login()
    cooksdict = requests.utils.dict_from_cookiejar(cookie)
    content = input("请输入说说内容：")
    qq = input("请输入你的QQ：")
    res = requests.get(url=f'https://user.qzone.qq.com/{qq}/infocenter', headers=headers,
                       cookies=cookie).text  # 获取qzonetoken的页面源码
    qzonetoken = re.findall('\{ try\{return "(.*?)";}', res)[0]  # 解析出qzonetoken
    g_tk = hash33(cooksdict['skey'], 5381)  # 从Cookie中获取g_tk
    url = f'https://user.qzone.qq.com/proxy/domain/taotao.qzone.qq.com/cgi-bin/emotion_cgi_publish_v6?qzonetoken={qzonetoken}&g_tk={g_tk}'
    data = {
        'syn_tweet_verson': '1',
        'paramstr': '1',
        'pic_template': '',
        'richtype': '',
        'richval': '',
        'special_url': '',
        'subrichtype': '',
        'who': '1',
        'con': content,
        'feedversion': '1',
        'ver': '1',
        'ugc_right': '1',
        'to_sign': '0',
        'hostuin': qq,
        'code_version': '1',
        'format': 'fs',
        'qzreferrer': 'https://user.qzone.qq.com/' + qq,
    }
    response = requests.post(url=url, headers=headers, data=data, cookies=cookie)
    print(response.status_code)


if __name__ == '__main__':
    send()