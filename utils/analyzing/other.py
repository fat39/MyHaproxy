# -*- coding:utf-8 -*-
from conf import settings

class OtherAnalyzer():

    name = "other"
    file = settings.FILES[name]["path"]

    def raw_context(self):

        """ do something """

        with open(self.file,encoding="utf-8") as f:
            print("[GET] other raw context")
            data = f.read()
            return data


    def create_item(self,items):

        """ do something"""

        print("OtherAnalyzer" + str(items))
        return "other create_item"


    def __new__(cls,):
        if not hasattr(cls,"_instance"):
            cls._instance = super(OtherAnalyzer, cls).__new__(cls)
        return cls._instance