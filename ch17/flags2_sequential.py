"""
下载多个国家的国旗 (包含错误处理代码)

依序下载版
"""
import collections

import requests
import tqdm

from flags2_common import main, save_flag, HTTPStatus, Result

DEFAULT_CONCUR_REQ = 1
MAX_CONCUR_REQ = 1

# BEGIN FALGS2_BASIC_HTTP_FUNCTIONS
def get_flag(base_url, cc):
  url = '{}/{cc}/{cc}.gif'.format(base_url, cc=cc.lower())
  resp = requests.get(url)
  if resp.status_code != 200:
    resp.raise_for_status()  # 当 HTTP 代码不是 200 时，使用此方法抛出异常
  return resp.content

def download_one(cc, base_url, verbose=False):
  try:
    image = get_flag(base_url, cc)
  except requests.exceptions.HTTPError as exc:  # 捕获 requests.exceptions.HTTPError 异常
    res = exc.response
    if res.status_code == 404:  # 特别处理 HTTP 404 错误
      status = HTTPStatus.not_found  # HTTPStatus 为 Enum 对象
      msg = 'not found'
    else:  # 重新抛出其他 HTTPError 异常，这些异常会向上冒泡，传给调用方
      raise
  else:
    save_flag(image, cc.lower() + '.gif')
    status = HTTPStatus.ok
    msg = 'OK'

  if verbose:  # 通过 -v/--verbose 选项来选择是否显示国家代码和状态信息
    print(cc, msg)

  return Result(status, cc)
# END FLAGS2_BASIC_HTTP_FUNCTIONS


# BEGIN FLAGS2_DOWNLOAD_MANY_SEQUENTIAL
def download_many(cc_list, base_url, verbose, max_req):
  counter = collections.Counter()  # 用于统计不同状态的下载信息
  cc_iter = sorted(cc_list)  # 按字母顺序传入国家代码列表
  if not verbose:  # 如果不是详细模式，则借助 tqdm 来显示进度条动画
    cc_iter = tqdm.tqdm(cc_iter)
  for cc in cc_iter:
    try:
      res = download_one(cc, base_url, verbose)  # 不断调用 download_one 函数，执行下载
    except requests.exceptions.HTTPError as exc:  # 处理 get_flag 函数抛出的与 HTTP 有关的且 download_one 没有处理的异常
      error_msg = 'HTTP error {res.status_code} - {res.reason}'
      error_msg = error_msg.format(res=exc.response)
    except requests.exceptions.ConnectionError as exc:
      error_msg = 'Connection error'
    else:
      error_msg = ''
      status = res.status

    if error_msg:
      status = HTTPStatus.error
    counter[status] += 1  # 以 HTTPStatus(一个 Enum) 中的值为键，增加计数器
    if verbose and error_msg:  # 如果是详细模式，则有错误，则显示带有当前国家代码的错误信息
      print('*** Error for {}:{}'.format(cc, error_msg))
  return counter
# END FLAGS2_DOWNLOAD_MANY_SEQEEN


if __name__ == '__main__':
  main(download_many, DEFAULT_CONCUR_REQ, MAX_CONCUR_REQ)
