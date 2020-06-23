import os
import time
import sys

import requests

POP20_CC = ('CN IN US ID BR PK NG BD RU JP MX PH VN ET EG DE IR TR CD FR ').split()  # 人口最多的 20 个国家的 ISO 3166 国家代码，按人口数据降序排列

BASE_URL = 'http://localhost:8002/flags'

DEST_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)),'downloads/') 


def save_flag(img, filename):
  """
  把 img (字节序列) 保存到 DEST_DIR 目录中，命名为 filename
  """
  path = os.path.join(DEST_DIR, filename)
  with open(path, 'wb') as fp:
    fp.write(img)


def get_flag(cc):
  """
  下载指定国家代码 (cc) 的国旗图像，返回响应中的二进制内容
  """
  url = '{}/{cc}/{cc}.gif'.format(BASE_URL, cc=cc.lower())
  resp = requests.get(url)
  return resp.content


def show(text):
  """
  显示一个字符串，然后刷新 sys.stdout，这样能在一行消息中看到进度
  """
  print(text, end=' ')
  sys.stdout.flush()


def download_many(cc_list):
  """
  按照字母表顺序迭代下载国家国旗，返回下载的国旗数量
  """
  for cc in sorted(cc_list):
    image = get_flag(cc)
    show(cc)
    save_flag(image, cc.lower() + '.gif')

  return len(cc_list)


def main(download_many):
  """
  main 函数记录并报告运行 download_many 函数之后的耗时
  """
  t0 = time.time()
  count = download_many(POP20_CC)
  elapsed = time.time() - t0
  msg = '\n{} flags download in {:.2f}s'
  print(msg.format(count, elapsed))


if __name__ == '__main__':
  main(download_many)
