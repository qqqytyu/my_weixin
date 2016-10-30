from wechat_sdk import WechatConf
import time
import fcntl
# import urllib
# import json
# import poster.encode
# from poster.streaminghttp import register_openers
# from basic import Basic

conf = WechatConf(
    token='weixin_langrensha',
    appid='wx9068ddea25a9c0d0',
    appsecret='242b90ea4fc787ce21345db3ce7ceae1',
    encrypt_mode='normal',  # 可选项：normal/compatible/safe，分别对应于 明文/兼容/安全 模式
    encoding_aes_key='qY71DJ7XdXsDWksumrazYMxf29gAKlopjOIB6n3pFV2'  # 如果传入此值则必须保证同时传入 token, appid
)
wechat = WechatBasic(conf=conf)  # 实例化 WechatBasic 官方接口类

while(True):
    access_token = wechat.get_access_token()
    f = open('AccessToken' , 'w' , encoding = 'utf-8')
    fcntl.flock(f , fcntl.LOCK_EX)
    f.write(access_token["access_token"]+'\n')
    f.write(access_token["access_token_expires_at"])
    fcntl.flock(f , fcntl.LOCK_UN)
    #batch_get(access_token["access_token"] , 'image')
    f.close()
    time.sleep(7000)

# def batch_get(self, accessToken, mediaType, offset=0, count=10):
#     postUrl = "https://api.weixin.qq.com/cgi-bin/material/batchget_material?access_token=%s" % accessToken
#     postData = '{ "type": "%s", "offset": %d, "count": %d }' % (mediaType, offset, count)
#     urlResp = urllib.request.urlopen(postUrl, postData.encode('utf-8'))
#     print(urlResp.read())

