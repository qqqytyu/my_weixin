from django.shortcuts import render
from django.http import HttpResponse
from WechatEncryption.admin import checkSignature , wechat_main
from django.views.decorators.csrf import csrf_exempt 


# Create your views here.

@csrf_exempt
def index(request):
    if request.method=='GET':
        if (checkSignature(request)):
            return HttpResponse(request.GET.get('echostr', None))
        else:
            return HttpResponse('weixin erro')
    else:
        HttpResponse(wechat_main(request))