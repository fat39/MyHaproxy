


import requests
import json

url = "http://127.0.0.1:8888/haproxy/"

data = {
    "data":json.dumps({
        'title': 'ssdfasdfsdfsdfsdfsdf',
        'record': [
            {
                'aaaaaaaaaaaa': 'bbbbbbbbb',
                'kkkk': 'vvvvvvv',
            },
        ]
    }),
}

ret = requests.post(url,data=data)
print(ret.text)