# -*- coding:utf-8 -*-
from conf import settings
from collections import OrderedDict


__filename__ = "haproxy"


class Block(object):
    def __init__(self, father=""):
        self.father = father
        self.children = {}

    def __str__(self):
        return "[BLOCK] {}".format(self.father)

    __repr__ = __str__


class Line(object):
    def __init__(self, line, index=0):
        self.line = line.strip("\n")  # 去除换行符
        self.index = index

    @property
    def is_total_blank(self):
        # 空白行
        return True if not self.line.strip() else False

    @property
    def has_pre_blank(self):
        # 前面有空格
        return True if not self.is_total_blank and self.line.startswith(" ") else False

    @property
    def has_note(self):
        # 有#
        return True if "#" in self.line else False

    @property
    def has_context(self):
        # 有真正的内容，无论是title和content
        return True if not self.is_total_blank and not self.line.lstrip().startswith("#") else False

    @property
    def is_pure_note(self):
        # 纯#
        return True if self.line.strip().startswith("#") else False

    @property
    def is_content(self):
        # 是每个title下面的内容，有内容
        return True if self.has_context and self.has_pre_blank else False

    @property
    def is_title(self):
        # 是title，有内容
        return True if self.has_context and not self.has_pre_blank else False

    @property
    def context(self):
        # 正文
        if self.is_content or self.is_title:
            context = self.line.split("#")[0].strip()
        else:
            context = ""
        return context

    @property
    def note(self):
        # 备注
        if self.has_note:
            note = self.line.split("#", 1)[1].strip()
        else:
            note = ""
        return note

    def __str__(self):
        if self.has_context and self.has_note:
            text = "{} # {}".format(self.context, self.note)
        elif self.has_context:
            text = "{}".format(self.context)
        elif self.has_note:
            text = "# {}".format(self.note)
        else:
            text = ""

        if self.has_pre_blank:
            text = "    " + text

        text = text.rstrip() + "\n"

        return "[LINE] {}".format(text)

    __repr__ = __str__


class Haproxy(object):

    @classmethod
    def obj_handle(cls,obj):
        raw_text = ""
        lines_odict = OrderedDict()
        blocks_odict = OrderedDict()
        b = Block()
        blocks_odict[b.father] = b
        for index,line in enumerate(obj):
            raw_text += line
            l = Line(line=line,index=index)
            lines_odict[l.context or l.index] = l
            if not l.is_title:
                b.children[l.context or l.index] = l
            else:
                b = Block(father=l.context)
                blocks_odict[b.father] = b

        obj = cls()
        obj.raw_text = raw_text
        obj.lines_odict = lines_odict
        obj.blocks_odict = blocks_odict

        return obj


    @classmethod
    def init_from_file(cls,file_path,coding="utf-8"):
        print(file_path)
        with open(file_path, encoding=coding) as f_obj:
            haproxy_obj =  cls.obj_handle(f_obj)
            haproxy_obj.file_path = file_path
        return haproxy_obj

    @classmethod
    def init_from_dict(cls,kwargs):
        print(kwargs)
        lines_list = []
        title = kwargs["title"]
        lines_list.append(title)
        content_list = kwargs["record"]
        tmp = []
        for content in content_list:
            for k,v in content.items():
                tmp.append("{k} {v}".format(k=k,v=v))
            lines_list.append("    " + " ".join(tmp))
        haproxy_obj = cls.obj_handle(lines_list)

        return haproxy_obj

    # def __str__(self):
    #     return "[FILE] {}".format(self.file_path)



class HaproxyAnalyzer():

    file = settings.FILES[__filename__]["path"]

    def raw_context(self):

        """ do something """

        print("[GET] haproxy raw context")
        hf = Haproxy.init_from_file(file_path=self.file)
        return hf.raw_text


    def create_item(self,items):

        """ do something"""
        content_str = Haproxy.init_from_dict(items)
        print(content_str)

        print("HaproxyAnalyzer" + str(items))
        return "haproxy create_item"


    def __new__(cls,):
        if not hasattr(cls,"_instance"):
            cls._instance = super(HaproxyAnalyzer, cls).__new__(cls)
        return cls._instance