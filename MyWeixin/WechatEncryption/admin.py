from django.contrib import admin
import hashlib
from wechat_sdk import WechatBasic
from wechat_sdk.exceptions import ParseError
from wechat_sdk.messages import TextMessage
from wechat_sdk import WechatConf
import random
# Register your models here.

#微信认证
def checkSignature(request , wechat):
    # #获取signature timestamp nonce echostr 参数
    # signature = request.GET.get('signature', None)
    # timestamp = request.GET.get('timestamp', None)
    # nonce = request.GET.get('nonce', None)
    # echostr = request.GET.get('echostr', None)
    # #定义token参数
    # token = 'weixin_langrensha'
    # #生成token timestamp nonce 字符串
    # tmplist = [token, timestamp, nonce]
    # tmplist.sort()
    # tmpstr = "%s%s%s" % tuple(tmplist)
    # #对字符串进行sha1加密
    # tmpstr = hashlib.sha1(tmpstr.encode('utf-8')).hexdigest()
    # if(tmpstr == signature):
    #     return True
    # else:
    #     return False

    signature = request.GET.get('signature', None)
    timestamp = request.GET.get('timestamp', None)
    nonce = request.GET.get('nonce', None)

    if not wechat.check_signature(signature=signature, timestamp=timestamp, nonce=nonce):
        return False
    else:
        return True

#消息判断
def wechat_main(request , wechat):

    body_text = request.body #提取body
    #msg_signature = request.GET.get('msg_signature', None)
    #timestamp = request.GET.get('timestamp', None)
    #nonce = request.GET.get('nonce', None)
    try:
        #wechat.parse_data(data = body_text , msg_signature=msg_signature, timestamp=timestamp, nonce=nonce) #解析body
        wechat.parse_data(data = body_text)
    except Exception as ex:
        print(ex)

    xml = ''
    type = wechat.message.type  # 对应于 XML 中的 MsgType（类型）
    if(type == 'subscribe'):
        str = '欢迎关注，回复功能查看目前所功能'
        xml = wechat.response_text(content=str)
    elif(type == 'unsubscribe'):
        pass    
    elif(type == 'text'):
        # source = wechat.message.source  # 对应于 XML 中的 FromUserName（目的）
        content = wechat.message.content  # 对应于 XML 中的 Content（内容）
        xml = reply_wechat_text(content , wechat)
    else:
        str = '您发送的内容类型为：%s , 目前还未开通此类型的回复 T.T' % type
        xml = wechat.response_text(content=str)
    return xml

#内容回复
def reply_wechat_text(content , wechat):
    if(content == '功能'):
        str = '1.计算器(例：计算 1 + 1) \n 2.学舌(例：学舌 学舌) \n'
        return wechat.response_text(content=str)
    else:
        content = content.split(' ' , 1)
        if(content[0] == '计算器'):
            num = count(content[1])
            str = '%s = %s' % (content[1] , num)
            return wechat.response_text(content=str)
        elif(content[0] == '学舌'):
            return wechat.response_text(content=content[1])
        # elif(content[0] == '趣图'):
        #     str = picture()
        #     return wechat.response_image(media_id=str)
        else:
            str = '你再说什么，我听不懂...'
            return wechat.response_text(content=str)
#计算
def count(content):
    content = content.split(' ')
    try:
        if(content[1] == '+'):
            return int(content[0]) + int(content[2])
        elif(content[1] == '-'):
            return int(content[0]) - int(content[2])
        elif(content[1] == '*'):
            return int(content[0]) * int(content[2])
        elif(content[1] == '/'):
            return int(content[0]) / int(content[2])
    except Exception as ex :
        return '我才一年级，复杂的计算我还不会 T.T'
