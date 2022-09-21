# -*- coding = utf-8 -*-
# 若需要在短时间内大量推送消息，请自行更改代码，把获取的access_token保存起来使用
# access_token有效期目前是7200s，可以通过api返回信息查到有效时间
# 不要频繁调用api获取，会被腾讯拉黑的
import requests
 
 
def push_service(corpid, corpsecret, Agentid):
    if corpid == "" or corpsecret == "" or Agentid == "":
        print("必要参数为空")
        return
 
    # 获取access_token
    url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corpid}&corpsecret={corpsecret}"
    r = requests.get(url).json()
    if r["errcode"] != 0:
        print(r["errmsg"])
        print("access_token获取失败！")
        return
    else:
        access_token = r["access_token"]
 
    # 获取图片media_id
    url = f"https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token={access_token}&type=image"
    img = requests.get('https://api.03c3.cn/zb').content
    files = {'media': img}
    response = requests.post(url=url, files=files).json()
    media_id = response["media_id"]
 
    # 推送
    url = f'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}'
    data = {
        "touser": "@all",
        "msgtype": "image",
        "agentid": Agentid,
        "image": {
            "media_id": media_id
        }
    }
    msg = requests.post(url=url, json=data).json()
    if msg["errcode"] != 0:
        print(f"推送失败!\n{msg}")
    else:
        print('推送成功')
 
 