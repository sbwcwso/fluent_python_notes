import asyncio
import collections
import os

import aiohttp
from aiohttp import web
import tqdm

from ch17.flags2_common import main, HTTPStatus, Result, save_flag

DEST_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)),'downloads/')
# 默认设为较小的值，防止远程网站出错
DEFAULT_CONCUR_REQ = 5
MAX_CONCUR_REQ = 1000

class FetchError(Exception):
  """
  自定义异常，用于包装其他 HTTP 或网络异响，并获取 country_code，以便报告错误
  """
  def __init__(self, country_code):
    self.country_code = country_code

  
async def get_flag(session, base_url, cc): 
  url = '{}/{cc}/{cc}.gif'.format(base_url, cc=cc.lower())
  async with session.get(url) as resp:
    if resp.status == 200:
      return await resp.read()
    elif resp.status == 404:
      raise web.HTTPNotFound()
    else:
      resp.raise_for_status()


async def download_one(session, cc, base_url, semaphore, verbose):
  """
  semaphore 是 asyncio.Semaphore 类的实例，Semaphore 类是同步装置，用于限制并发请求数量
  """
  try:
    with await semaphore:  # 在 await 中将 semaphore 当做上下文管理器使用，防止阻塞整个系统，如果 semaphore 超过所允许的最大值，则只有这个协程会阻塞
      image = await get_flag(session, base_url, cc)  # 退出此 with 语句后，semaphore 计数器会递减，解除阻塞可能等待同一个 semaphore 对象的其它协程实例
  except web.HTTPNotFound:
    status = HTTPStatus.not_found
  except Exception as exc:
    raise FetchError(cc) from exc  # raise X from Y, 链接原来的异常： https://www.python.org/dev/peps/pep-3134/
  else:
    save_flag(image, cc.lower() + '.gif', DEST_DIR)
    status = HTTPStatus.ok
    msg = 'OK'
  if verbose and msg:
    print(cc, msg)
  
  return Result(status, cc)



async def downloader_coro(cc_list, base_url, verbose, concur_req):
  """
  类似于 download_many，但是是协程函数，不能直接调用
  """
  counter = collections.Counter()
  semaphore = asyncio.Semaphore(concur_req)  # 设置最多允许激活的协程数目

  # 根据文档 https://docs.aiohttp.org/en/stable/client_quickstart.html#make-a-request，一个程序最好只使用一个 Session
  # setting the client to tell the server to close the connection after each request https://github.com/aio-libs/aiohttp/issues/850#issuecomment-471663047
  async with aiohttp.ClientSession(headers={"Connection": "close"}) as session:  
    to_do = [download_one(session, cc, base_url, semaphore, verbose)
            for cc in sorted(cc_list)]  # 创建一个协程对象列表
    to_do_iter = asyncio.as_completed(to_do)  # 获取一个迭代器，此迭代器会在  funture 运行结束后返回 future
  
    if not verbose:
      to_do_iter = tqdm.tqdm(to_do_iter, total=len(cc_list))  # 将迭代器传给 tqdm，以显示进度条
    for future in to_do_iter:  # 迭代运行结束的 future
      try:
        res = await future  # 获取 future 的运行结果
      except FetchError as exc:
        country_code = exc.country_code  # 获取国家代码 
        try:
          error_msg = 'HTTP error {resp.status} - {resp.message}'
          error_msg = error_msg.format(resp=exc.__cause__)
        except Exception:  # 如果异常中没有消息，使用链接异常的类名作为消息
          error_msg = exc.__cause__.__class__.__name__  
        if verbose and error_msg:
          msg = '*** Error for {}: {}'
          print(msg.format(country_code, error_msg))
        status = HTTPStatus.error
      else:
        status = res.status
      counter[status] += 1
  return counter


def download_many(cc_list, base_url, verbose, concur_req):
  loop = asyncio.get_event_loop()
  coro = downloader_coro(cc_list, base_url, verbose, concur_req)
  counts = loop.run_until_complete(coro)
  loop.close()

  return counts


if __name__ == '__main__':
  main(download_many, DEFAULT_CONCUR_REQ, MAX_CONCUR_REQ)
