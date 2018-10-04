# -*- coding:utf-8 -*-
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))




FILES = {
    "haproxy":{
        "path":os.path.join(BASE_DIR,"data","haproxy")
    },
    "other": {
        "path": os.path.join(BASE_DIR, "data", "other")
    },
}


ANALYZER = {
    "haproxy":"utils.analyzing.haproxy.HaproxyAnalyzer",
    "other":"utils.analyzing.other.OtherAnalyzer",
}
