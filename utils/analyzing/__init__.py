# -*- coding:utf-8 -*-
from conf import settings
from importlib import import_module


class MyAnalyzer(object):

    def myanalyzer(self,file):
        return self.analyzers[file]

    @property
    def analyzers(self):
        analyzers = {}
        for name,cls_path in settings.ANALYZER.items():
            module_path,cls_name = cls_path.rsplit(".",1)
            _module = import_module(module_path)
            if hasattr(_module,cls_name):
                cls = getattr(_module,cls_name)
                if hasattr(cls, 'initial'):
                    obj = cls.initial()
                else:
                    obj = cls()
                analyzers[name] = obj
        return analyzers

    # def __new__(cls, *args, **kwargs):
    #     """ 单例模式"""
    #     if not hasattr(cls,"_instance"):
    #         cls._instance = super(MyAnalyzing, cls).__new__(cls)
    #     return cls._instance

myanalyzer = MyAnalyzer()