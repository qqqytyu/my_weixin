from django.contrib import admin
from lxml import etree
from django.utils.encoding import smart_str
import hashlib
from wechat_sdk import WechatBasic
from wechat_sdk.exceptions import ParseError
from wechat_sdk.messages import TextMessage
from wechat_sdk import WechatConf
# Register your models here.

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
    if(type == 'event'):
        Event = wechat.message.event
        if(Event == 'subscribe'):
            str = '欢迎关注，回复功能查看目前所功能'
            xml = wechat.response_text(content=str)
    else:
        id = wechat.message.id  # 对应于 XML 中的 MsgId
        target = wechat.message.target  # 对应于 XML 中的 ToUserName(原)
        source = wechat.message.source  # 对应于 XML 中的 FromUserName（目的）
        time = wechat.message.time  # 对应于 XML 中的 CreateTime
        content = wechat.message.content  # 对应于 XML 中的 Content（内容）
        raw = wechat.message.raw  # 原始 XML 文本，方便进行其他分析
        str = '''
        来自 = %s
        格式 = %s
        ''' % (source , type)
        xml = wechat.response_text(content = str)
    return xml