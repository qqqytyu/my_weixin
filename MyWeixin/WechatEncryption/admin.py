from django.contrib import admin
from lxml import etree
from django.utils.encoding import smart_str
# Register your models here.

def checkSignature(request):
    #获取signature timestamp nonce echostr 参数
    signature = request.GET.get('signature', None)
    timestamp = request.GET.get('timestamp', None)
    nonce = request.GET.get('nonce', None)
    echostr = request.GET.get('echostr', None)
    #定义token参数
    token = 'weixin_langrensha'
    #生成token timestamp nonce 字符串
    tmplist = [token, timestamp, nonce]
    tmplist.sort()
    tmpstr = "%s%s%s" % tuple(tmplist)
    #对字符串进行sha1加密
    tmpstr = hashlib.sha1(tmpstr).hexdigest()
    if(tmpstr == signature):
        return True
    else:
        return False

def wechat_main(request):
    xmlstr = smart_str(request.body)
    xml = etree.fromstring(xmlstr)
    ToUserName = xml.find('ToUserName').text
    FromUserName = xml.find('FromUserName').text
    CreateTime = xml.find('CreateTime').text
    MsgType = xml.find('MsgType').text
    Content = xml.find('Content').text
    MsgId = xml.find('MsgId').text
    reply_xml = """
           <xml>
           <ToUserName><![CDATA[%s]]></ToUserName>
           <FromUserName><![CDATA[geeks_at_qdu]]></FromUserName>
           <CreateTime>12345678</CreateTime>
           <MsgType><![CDATA[text]]></MsgType>
           <Content><![CDATA[%s]]></Content>
           </xml>""" % (FromUserName, Content + "  Hello world, this is test message")
    print(ToUserName +'\n'+ FromUserName +'\n'+ CreateTime +'\n'+ MsgType +'\n'+ Content +'\n'+ MsgId)