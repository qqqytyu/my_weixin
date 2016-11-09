from django.contrib import admin
from wechat_sdk import WechatBasic
from wechat_sdk.exceptions import ParseError
from wechat_sdk.messages import TextMessage
from wechat_sdk import WechatConf
import hashlib ,random,json,urllib.request
#天气图片字典
weather_dict = {
'晴':'http://files.heweather.com/cond_icon/100.png',
'多云':'http://files.heweather.com/cond_icon/101.png',
'少云':'http://files.heweather.com/cond_icon/102.png',
'晴间多云':'http://files.heweather.com/cond_icon/103.png',
'阴':'http://files.heweather.com/cond_icon/104.png',
'有风':'http://files.heweather.com/cond_icon/200.png',
'平静':'http://files.heweather.com/cond_icon/201.png',
'微风':'http://files.heweather.com/cond_icon/202.png',
'和风':'http://files.heweather.com/cond_icon/203.png',
'清风':'http://files.heweather.com/cond_icon/204.png',
'强风/劲风':'http://files.heweather.com/cond_icon/205.png',
'疾风':'http://files.heweather.com/cond_icon/206.png',
'大风':'http://files.heweather.com/cond_icon/207.png',
'烈风':'http://files.heweather.com/cond_icon/208.png',
'风暴':'http://files.heweather.com/cond_icon/209.png',
'狂爆风':'http://files.heweather.com/cond_icon/210.png',
'飓风':'http://files.heweather.com/cond_icon/211.png',
'龙卷风':'http://files.heweather.com/cond_icon/212.png',
'热带风暴':'http://files.heweather.com/cond_icon/213.png',
'阵雨':'http://files.heweather.com/cond_icon/300.png',
'强阵雨':'http://files.heweather.com/cond_icon/301.png',
'雷阵雨':'http://files.heweather.com/cond_icon/302.png',
'强雷阵雨':'http://files.heweather.com/cond_icon/303.png',
'雷阵雨伴有冰雹':'http://files.heweather.com/cond_icon/304.png',
'小雨':'http://files.heweather.com/cond_icon/305.png',
'中雨':'http://files.heweather.com/cond_icon/306.png',
'大雨':'http://files.heweather.com/cond_icon/307.png',
'极端降雨':'http://files.heweather.com/cond_icon/308.png',
'毛毛雨/细雨':'http://files.heweather.com/cond_icon/309.png',
'暴雨':'http://files.heweather.com/cond_icon/310.png',
'大暴雨':'http://files.heweather.com/cond_icon/311.png',
'特大暴雨':'http://files.heweather.com/cond_icon/312.png',
'冻雨':'http://files.heweather.com/cond_icon/313.png',
'小雪':'http://files.heweather.com/cond_icon/400.png',
'中雪':'http://files.heweather.com/cond_icon/401.png',
'大雪':'http://files.heweather.com/cond_icon/402.png',
'暴雪':'http://files.heweather.com/cond_icon/403.png',
'雨夹雪':'http://files.heweather.com/cond_icon/404.png',
'雨雪天气':'http://files.heweather.com/cond_icon/405.png',
'阵雨夹雪':'http://files.heweather.com/cond_icon/406.png',
'阵雪':'http://files.heweather.com/cond_icon/407.png',
'薄雾':'http://files.heweather.com/cond_icon/500.png',
'雾':'http://files.heweather.com/cond_icon/501.png',
'霾':'http://files.heweather.com/cond_icon/502.png',
'扬沙':'http://files.heweather.com/cond_icon/503.png',
'浮尘':'http://files.heweather.com/cond_icon/504.png',
'沙尘暴':'http://files.heweather.com/cond_icon/507.png',
'强沙尘暴':'http://files.heweather.com/cond_icon/508.png',
'热':'http://files.heweather.com/cond_icon/900.png',
'冷':'http://files.heweather.com/cond_icon/901.png',
'未知':'http://files.heweather.com/cond_icon/999.pn'
}

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
    try:
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
        content = wechat.message.content  # 对应于 XML 中的 Content（内容）
        xml = reply_wechat_text(content , wechat)
    else:
        str = '您发送的内容类型为：%s , 目前还未开通此类型的回复 T.T' % type
        xml = wechat.response_text(content=str)
    return xml

#内容回复
def reply_wechat_text(content , wechat):
    con = content.split(' ')
    if(con[0] == '功能'):
        str = '1.基本信息\n2.天气预报'
        return wechat.response_text(content=str)
    elif(con[0] == '基本信息'):
        id = wechat.message.id  # 对应于 XML 中的 MsgId
        target = wechat.message.target  # 对应于 XML 中的 ToUserName
        source = wechat.message.source  # 对应于 XML 中的 FromUserName
        time = wechat.message.time  # 对应于 XML 中的 CreateTime
        type = wechat.message.type  # 对应于 XML 中的 MsgType
        str = "id = %s\nToUserName = %s\nFromUserName = %s\nCreateTime = %s\nMsgType = %s\n" % (id,target,source,time,type)
        return wechat.response_text(content=str)
    elif(con[0] == '天气预报'):
        str = "请输入：天气 地点"
        return wechat.response_text(content=str)
    elif(con[0] == '天气'):
        return BackWeather(con[1] , wechat)

def BackWeather(con , wechat):
    #url = "https://free-api.heweather.com/v5/weather?city=%s&key=57d01b5cee324a80b947f0f994dcabc0" % con.encode('gbk')
    url = "https://free-api.heweather.com/v5/weather?city=%E5%8C%97%E4%BA%AC&key=57d01b5cee324a80b947f0f994dcabc0"
    date = ((urllib.request.urlopen(url)).read()).decode('utf-8')
    jsonDate = json.loads(date)
    print(jsonDate)
    xml = wechat.response_news([
        {
            'title': u'%s(实时)天气情况' % jsonDate["HeWeather5"][0]["basic"]["update"]["loc"],
            'description': u'%s' % jsonDate["HeWeather5"][0]["now"]["cond"]["txt"],
            'picurl': u'%s' % weather_dict[jsonDate["HeWeather5"][0]["now"]["cond"]["txt"]],
            'url': u'http://www.weather.com.cn/weather/101030100.shtml',
        }
    ])
    return xml
