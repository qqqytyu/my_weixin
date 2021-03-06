from wechat_sdk import WechatConf
from wechat_sdk import WechatBasic
from wechat_sdk.exceptions import ParseError
from wechat_sdk.messages import TextMessage
import time
import fcntl
conf = WechatConf(
    token='weixin_langrensha',
    appid='wx40204f4d0ec2ea5a',
    appsecret='451bc8bf5e759c596256cade2e11e42d',
    encrypt_mode='normal',  # 可选项：normal/compatible/safe，分别对应于 明文/兼容/安全 模式
    encoding_aes_key='qY71DJ7XdXsDWksumrazYMxf29gAKlopjOIB6n3pFV2'  # 如果传入此值则必须保证同时传入 token, appid
)
wechat = WechatBasic(conf=conf)  # 实例化 WechatBasic 官方接口类

while(True):
    access_token = wechat.get_access_token()
    f = open('AccessToken' , 'w' , encoding = 'utf-8')
    fcntl.flock(f , fcntl.LOCK_EX)
    f.write(access_token["access_token"]+'\n')
    f.write(str(access_token["access_token_expires_at"]))
    fcntl.flock(f , fcntl.LOCK_UN)
    #batch_get(access_token["access_token"] , 'image')
    f.close()
    time.sleep(3500)

# def batch_get(self, accessToken, mediaType, offset=0, count=10):
#     postUrl = "https://api.weixin.qq.com/cgi-bin/material/batchget_material?access_token=%s" % accessToken
#     postData = '{ "type": "%s", "offset": %d, "count": %d }' % (mediaType, offset, count)
#     urlResp = urllib.request.urlopen(postUrl, postData.encode('utf-8'))
#     print(urlResp.read())

