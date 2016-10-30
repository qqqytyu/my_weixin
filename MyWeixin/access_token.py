from wechat_sdk import WechatConf
import time
import fcntl
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
    f.close()
    time.sleep(7000)

