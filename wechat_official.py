from flask import Flask
from flask import render_template
from flask import redirect
from flask import request
import hashlib
import xml.etree.cElementTree as et
import reply_templates
import time

app = Flask(__name__)


@app.route('/wx', methods=['POST', 'GET'])
def wechat():
    if request.method == 'GET':
        # 微信公众平台填写的token
        token = 'fengjiali'
        # 获取输入参数
        data = request.args
        timestamp = data.get('timestamp')
        signature = data.get('signature')
        nonce = data.get('nonce')
        echostr = data.get('echostr')
        # 计算hash用于验证服务器请求
        list = [token, timestamp, nonce]
        list.sort()
        s = list[0] + list[1] + list[2]
        hashcode = hashlib.sha1(s.encode('utf-8')).hexdigest()
        if hashcode == signature:
            return echostr
        else:
            return ""
    if request.method == 'POST':
        xmldata = request.stream.read()
        # print(type(xmldata))
        xml_rec = et.fromstring(xmldata)
        # assert isinstance(xml_rec, str)
        ToUserName = xml_rec.find('ToUserName').text
        fromUser = xml_rec.find('FromUserName').text
        MsgType = xml_rec.find('MsgType').text
        Content = xml_rec.find('Content').text
        MsgId = xml_rec.find('MsgId').text
        print ('收到消息：'+Content)
        # print(type((reply_templates.reply_template(MsgType) % (fromUser, ToUserName, int(time.time()), Content)).encode('utf-8')))
        return ((reply_templates.reply_template(MsgType) % (fromUser, ToUserName, int(time.time()), Content)).encode('utf-8'))
        # print(b'<xml><ToUserName><![CDATA[oOGio0aHgOm8styibLmXT3ll-EIM]]></ToUserName>\n<FromUserName><![CDATA[gh_b1f6a2bbaabb]]></FromUserName>\n<CreateTime>1527945486</CreateTime>\n<MsgType><![CDATA[text]]></MsgType>\n<Content><![CDATA[To]]></Content>\n<MsgId>6562475892902749464</MsgId>\n</xml>')


if __name__ == '__main__':
    app.run('0.0.0.0', 80)
