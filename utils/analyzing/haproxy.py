# -*- coding:utf-8 -*-
from conf import settings
from collections import OrderedDict
import copy
import time

__filename__ = "haproxy"
file_path = settings.FILES[__filename__]["path"]


class Block(object):
    def __init__(self, father=""):
        self.father = father or Line(father)
        self.children = OrderedDict()

    @property
    def raw_text(self):
        ret = (self.father.raw_text) if self.father.raw_text else ""
        for k,child in self.children.items():
            ret += child.raw_text
        return ret

    def __str__(self):
        return "[BLOCK] {}".format(self.father)

    __repr__ = __str__


class Line(object):

    def __init__(self, raw_text, index=0):
        self.raw_text = raw_text
        self.index = index

    @property
    def line(self):
        return self.raw_text.strip("\n")  # 去除换行符

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

    @property
    def raw_text(self):
        tmp = ""
        for k,line in self.lines_odict.items():
            tmp += line.raw_text

        return tmp

    @classmethod
    def obj_handle(cls,obj):
        lines_odict = OrderedDict()
        blocks_odict = OrderedDict()
        b = Block()  # file的头部block，可能没有father
        blocks_odict[b.father] = b
        for index,line in enumerate(obj):
            l = Line(raw_text=line,index=index)
            lines_odict[l.context or l.index] = l
            if not l.is_title:
                b.children[l.context or l.index] = l
            else:
                b = Block(father=l)
                blocks_odict[l.context] = b


        obj = cls()
        obj.lines_odict = lines_odict
        obj.blocks_odict = blocks_odict

        return obj

    @classmethod
    def init_from_file(cls,file_path,coding="utf-8"):
        with open(file_path, encoding=coding) as f_obj:
            haproxy_obj =  cls.obj_handle(f_obj)
            haproxy_obj.file_path = file_path
        return haproxy_obj

    @classmethod
    def init_from_dict(cls,kwargs):
        print(kwargs)
        lines_list = []
        title = kwargs["title"]
        lines_list.append(title + "\n")
        content_list = kwargs["record"]
        tmp = []
        for content in content_list:
            for k,v in content.items():
                tmp.append("{k} {v}".format(k=k,v=v))
            lines_list.append("    {}\n".format(" ".join(tmp)))
        haproxy_obj = cls.obj_handle(lines_list)

        return haproxy_obj

    @classmethod
    def init_from_mul_obj(cls,base_obj,*objs):
        if not objs:return base_obj
        return cls.merge_mul_objs(base_obj,*objs)

    @classmethod
    def merge_mul_objs(cls,base_obj,*objs):
        new_obj = copy.deepcopy(base_obj)
        for obj in objs:
            for base_k,base_v in base_obj.__dict__.items():
                if isinstance(base_v,OrderedDict):  # 暂时制作ordereddict
                    obj_v = getattr(obj,base_k,None)
                    new_obj.__dict__[base_k].update(obj_v or {})  # 如果objs里没有某个字段，比如file_path，则不要
                else:  # 暂时制作ordereddict
                    continue
        # print(dir(base_obj))
        # print(dir(new_obj))
        return new_obj

    def bak_file(self):
        pass

    def dump_file(self,file_path,coding="utf-8"):
        with open(file_path, encoding=coding, mode="w") as f_obj:
            for k,line_obj in self.lines_odict.items():

                f_obj.write(line_obj.raw_text if line_obj.raw_text.endswith("\n") else line_obj.raw_text+"\n")



class HaproxyAnalyzer():
    haproxy = Haproxy

    def get_obj(self):
        print("[GET] haproxy raw context")
        hp_obj = self.haproxy.init_from_file(file_path=file_path)
        return hp_obj

    def create_obj(self,items):

        """ do something"""

        create_hp_obj = self.haproxy.init_from_dict(items)
        origin_hp_obj = self.get_obj()
        new_hp_obj = self.haproxy.init_from_mul_obj(origin_hp_obj,create_hp_obj)
        # print("HaproxyAnalyzer" + str(items))
        new_hp_obj.dump_file(file_path)
        return new_hp_obj



    def __new__(cls,):
        if not hasattr(cls,"_instance"):
            cls._instance = super(HaproxyAnalyzer, cls).__new__(cls)
        return cls._instance