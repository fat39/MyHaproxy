# # -*- coding:utf-8 -*-

from collections import OrderedDict

class File(object):

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

    def __init__(self,file_path,coding="utf-8"):
        self.file_path = file_path
        self.coding = coding

        self.file_handle()

    def file_handle(self):
        raw_text = ""
        lines_odict = OrderedDict()
        blocks_odict = OrderedDict()
        b = self.Block()
        blocks_odict[b.father] = b
        with open(self.file_path,encoding=self.coding) as f:
            for index,line in enumerate(f):
                raw_text += line
                l = self.Line(line=line,index=index)
                lines_odict[l.context or l.index] = l
                if not l.is_title:
                    b.children[l.context or l.index] = l
                else:
                    b = self.Block(father=l.context)
                    blocks_odict[b.father] = b

        self.raw_text = raw_text
        self.lines_list = lines_odict
        self.blocks_list = blocks_odict


    def __str__(self):
        return "[FILE] {}".format(self.file_path)


file = "data/haproxy"
f = File(file_path=file)
print(f.lines_list["option redispatch"])













# print(f.lines_list)
# print(f.blocks_list)

# for line in f.lines_list:
#     print(line.__dict__)
#     pass
# with open(file,encoding="utf-8") as f:
#     with open("test1.txt","w") as f1:
#         for line in f:
#             l = Line(line)
#             print(l.__dict__)


#
# x = """
# # adfadsfas
# [Diag]  # sdfadf
# LastTime=1538122031  # adfasdf
# [SmartBuf]
# MaxTime=3  # adfasdf
# MinTime=1
# AvgTime=2
# MaxNormalTime=6
# MinNormalTime=2
# AvgNormalTime=4
# """
# import configparser
#
# config = configparser.ConfigParser()
# config.read_string(x)
# print(config.items("SmartBuf"))



