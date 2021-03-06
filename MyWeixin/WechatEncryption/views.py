from django.shortcuts import render
from django.http import HttpResponse
from WechatEncryption.admin import checkSignature , wechat_main
from django.views.decorators.csrf import csrf_exempt 
from wechat_sdk import WechatBasic
from wechat_sdk.exceptions import ParseError
from wechat_sdk.messages import TextMessage
from wechat_sdk import WechatConf
import fcntl

# Create your views here.

f =open('AccessToken' , 'r' , encoding = 'utf-8')
fcntl.flock(f , fcntl.LOCK_EX)#加锁
AccessToken = f.readlines()
fcntl.flock(f , fcntl.LOCK_UN)
f.close()
conf = WechatConf(
    token='weixin_langrensha',
    appid='wx40204f4d0ec2ea5a',
    appsecret='451bc8bf5e759c596256cade2e11e42d',
    encrypt_mode='normal',  # 可选项：normal/compatible/safe，分别对应于 明文/兼容/安全 模式
    encoding_aes_key='qY71DJ7XdXsDWksumrazYMxf29gAKlopjOIB6n3pFV2',  # 如果传入此值则必须保证同时传入 token, appid
    access_token=AccessToken[0],
    access_token_expires_at=AccessToken[1]
)
wechat = WechatBasic(conf=conf)  # 实例化 WechatBasic 官方接口类

@csrf_exempt
def index(request):
    if request.method=='GET':
        if (checkSignature(request , wechat)):
            return HttpResponse(request.GET.get('echostr', None))
        else:
            return HttpResponse('weixin erro')
    else:
        return HttpResponse(wechat_main(request , wechat))