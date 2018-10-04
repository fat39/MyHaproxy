# -*- coding:utf-8 -*-
from collections import OrderedDict

file = "data/haproxy"
with open(file,encoding="utf-8") as f:
    title_context = 0
    f_odict = OrderedDict()
    f_odict[title_context] = {"raw_text": None, "note": None, "context": title_context, "children": OrderedDict()}
    for index,line in enumerate(f):
        line_dict = {"raw_text":None,"note":None,"context":None,"children":None}
        line = line.strip("\n")  # 去除换行符
        line_dict["raw_text"] = line
        if not line.lstrip():
            # 换行
            f_odict[title_context]["children"][index] = line_dict
        else:
            # 该行必有东西,可能是标题、内容或者是纯#
            if line.lstrip().startswith("#"):
                # 是纯#
                line_dict["note"] = line.split("#", 1)[1].lstrip()
                f_odict[title_context]["children"][index] = line_dict

            elif not line.startswith(" "):
                # 是block的标题
                line_split = line.split("#", 1)
                title_context, note = (line_split[0],line_split[1]) if len(line_split) == 2 else (line_split[0], None)
                title_context = title_context.strip()
                note = note.strip() if note else None
                line_dict["note"] = note
                line_dict["context"] = title_context
                line_dict["children"] = OrderedDict()
                f_odict[title_context] = line_dict
            else:
                # 该行是children
                line_split = line.split("#", 1)
                child_context, note = (line_split[0], line_split[1]) if len(line_split) == 2 else (line_split[0], None)
                child_context = child_context.strip()
                note = note.strip() if note else None
                line_dict["note"] = note
                line_dict["context"] = child_context
                f_odict[title_context]["children"][child_context] = line_dict



with open("test1.txt","w",encoding="utf-8") as f:
    line1 = "{} # {}\n"
    line2 = "{}\n"
    line3 = "# {}\n"
    for title_name,title_dict in f_odict.items():
        if title_name:
            if title_dict["note"] and title_dict["context"]:
                line = line1.format(title_dict["note"],title_dict["context"])
            elif title_dict["context"]:
                line = line2.format(title_dict["context"])
            elif title_dict["note"]:
                line = line3.format(title_dict["note"])
            else:
                line = "\n"
            f.write(line)
        for k, line_dict in title_dict["children"].items():
            pre = "    " if title_name else ""
            if line_dict["note"] and line_dict["context"]:
                line = line1.format(line_dict["note"],line_dict["context"])
            elif line_dict["context"]:
                line = line2.format(line_dict["context"])
            elif line_dict["note"]:
                line = line3.format(line_dict["note"])
            else:
                line = "\n"
            line = pre + line
            # print(line)
            f.write(line)




#
# def fetch(backend):
#     backend_title = 'backend %s' % backend
#     record_list = []
#     with open(file,encoding="utf-8") as obj:
#         flag = False
#         for line in obj:
#             line = line.strip()
#             if line.startswith(backend_title):
#                 flag = True
#                 continue
#             if flag and line.startswith('backend'):
#                 flag = False
#                 break
#
#             if flag and line:
#                 record_list.append(line)
#
#     return record_list
#
# # print(fetch("php_server"))