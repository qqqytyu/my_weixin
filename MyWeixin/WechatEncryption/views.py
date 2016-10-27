from django.shortcuts import render
from django.http import HttpResponse
from WechatEncryption.admin import checkSignature
from django.views.decorators.csrf import csrf_exempt , wechat_main
import hashlib

# Create your views here.

@csrf_exempt
def index(request):
    if request.method=='GET':
        if (checkSignature(request)):
            return HttpResponse(request.GET.get('nonce', None))
        else:
            return HttpResponse('weixin erro')
    else:
        return HttpResponse(wechat_main(request))