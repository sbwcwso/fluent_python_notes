from urllib.request import urlopen
import warnings
import os
import json

URL = 'http://www.oreilly.com/pub/sc/osconfeed'
JSON = "ch19/data/osconfeed.json"


def load():
  if not os.path.exists(JSON):
    msg = 'download {} to {}'.format(URL, JSON)
    warnings.warn(msg)  # 如需下载，就发出提醒
    with urlopen(URL) as remote, open(JSON, 'wb') as local:  # 在 with 语句中使用两个上下文管理器，分别用于读取和保存远程文件
      local.write(remote.read())
  
  with open(JSON) as fp:
    return json.load(fp)  # 解析 JSON 文件，返回 Python 原生对象