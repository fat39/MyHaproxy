# -*- coding:utf-8 -*-
import tornado.ioloop
import tornado.web
from conf import settings
from utils.analyzing.haproxy import HaproxyAnalyzer
from utils.analyzing import myanalyzer
import json
import time

handler_settings = {
    "template_path":"template",
    "static_path":"static",
}

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        support_analyzer = settings.ANALYZER.keys() or None
        self.render("index.html",support_analyzer=support_analyzer)


class MainHandler(tornado.web.RequestHandler):
    def get(self,file):
        print("get")
        # self._headers.add('Access-Control-Allow-Origin',"*")
        # print(self._headers)
        # print(type(self._headers))
        ma = myanalyzer.myanalyzer(file)
        get_result = ma.raw_context()
        self.write(get_result)

    def post(self,file):
        """
        新增条目
        :param file: 格式是dict的json格式，如｛'a':1｝
        :return:
        """
        ma = myanalyzer.myanalyzer(file)
        data = self.get_argument("data")
        data = json.loads(data)
        post_result = ma.create_item(data)
        print("post")

        self.write(post_result)

    def patch(self,file):
        print("patch")
        self.write("patch")

    def put(self,file):
        print("put")
        self.write("put")

    def delete(self,file):
        print("delete")
        self.write("delete")


application = tornado.web.Application([
    (r"/index/$",IndexHandler),
    (r"/(?P<file>.+)/", MainHandler),
],**handler_settings)



if __name__ == "__main__":
    application.listen(8888)
    print("开始监听端口 http://127.0.0.1:8888")
    tornado.ioloop.IOLoop.instance().start()
