from django.shortcuts import render
from django.http import HttpResponse
from WechatEncryption.admin import checkSignature
from django.views.decorators.csrf import csrf_exempt
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
        return HttpResponse('Hello World')