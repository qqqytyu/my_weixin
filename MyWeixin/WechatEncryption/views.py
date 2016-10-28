from django.shortcuts import render
from django.http import HttpResponse
from WechatEncryption.admin import checkSignature , wechat_main
from django.views.decorators.csrf import csrf_exempt 
from wechat_sdk import WechatBasic
from wechat_sdk.exceptions import ParseError
from wechat_sdk.messages import TextMessage
from wechat_sdk import WechatConf


# Create your views here.

conf = WechatConf(
    token='weixin_langrensha',
    appid='wx9068ddea25a9c0d0',
    appsecret='242b90ea4fc787ce21345db3ce7ceae1',
    encrypt_mode='normal',  # 可选项：normal/compatible/safe，分别对应于 明文/兼容/安全 模式
    encoding_aes_key='qY71DJ7XdXsDWksumrazYMxf29gAKlopjOIB6n3pFV2'  # 如果传入此值则必须保证同时传入 token, appid
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