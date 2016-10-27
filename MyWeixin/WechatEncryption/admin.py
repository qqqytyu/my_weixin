from django.contrib import admin
from lxml import etree
from django.utils.encoding import smart_str
import hashlib
from wechat_sdk import WechatBasic
from wechat_sdk.exceptions import ParseError
from wechat_sdk.messages import TextMessage
from wechat_sdk import WechatConf
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
    tmpstr = hashlib.sha1(tmpstr.encode('utf-8')).hexdigest()
    if(tmpstr == signature):
        return True
    else:
        return False

def wechat_main(request):

    conf = WechatConf(
        token='weixin_langrensha',
        appid='wx9068ddea25a9c0d0',
        appsecret='242b90ea4fc787ce21345db3ce7ceae1',
        encrypt_mode='safe',  # 可选项：normal/compatible/safe，分别对应于 明文/兼容/安全 模式
        encoding_aes_key='qY71DJ7XdXsDWksumrazYMxf29gAKlopjOIB6n3pFV2'  # 如果传入此值则必须保证同时传入 token, appid
    )

    wechat = WechatBasic(conf=conf) #实例化 WechatBasic 官方接口类

    body_text = request.body #提取body
    try:
        wechat.parse_data(body_text) #解析body
    except Exception as ex:
        print(ex)

    id = wechat.message.id  # 对应于 XML 中的 MsgId
    target = wechat.message.target  # 对应于 XML 中的 ToUserName(原)
    source = wechat.message.source  # 对应于 XML 中的 FromUserName（目的）
    time = wechat.message.time  # 对应于 XML 中的 CreateTime
    type = wechat.message.type  # 对应于 XML 中的 MsgType（类型）
    content = wechat.message.content  # 对应于 XML 中的 Content（内容）
    raw = wechat.message.raw  # 原始 XML 文本，方便进行其他分析
    str = '''
    id = %s
    target = %s
    source = %s
    time = %s
    type = %s
    content = %s
    ''' % (id , target , source , time , type,content)
    xml = wechat.response_text(content = str)
    return xml