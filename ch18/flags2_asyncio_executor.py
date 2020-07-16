import asyncio
import os
import concurrent
import sys

from aiohttp import web

from ch17.flags2_common import main, HTTPStatus, Result, save_flag
from ch18.flags2_asyncio import FetchError, get_flag, DEFAULT_CONCUR_REQ, MAX_CONCUR_REQ, downloader_coro

DEST_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)),'downloads/')


async def download_one(session, cc, base_url, semaphore, verbose):
  try:
    with (await semaphore):
      image = await get_flag(session, base_url, cc)
  except web.HTTPNotFound:
    status = HTTPStatus.not_found
    msg = 'not found'
  except Exception as exc:
    raise FetchError(cc) from exc
  else:
    loop = asyncio.get_event_loop()  # 获取事件循环的对象引用
    loop.run_in_executor(None,  # 第一个参数是 Executor 实例，如果为 None，则使用事件循环的默认值，也可传入 concurrent.futures 中的 ThreadPoolExecutor 与 ProcessPoolExecutor
                           save_flag, image, cc.lower() + '.gif', DEST_DIR)  # 余下的参数是可调用对象，以及可调用对象的位置参数
    status = HTTPStatus.ok
    msg = 'OK'
  if verbose and msg:
    print(cc, msg)

  return Result(status, cc)


def download_many(cc_list, base_url, verbose, concur_req):
  loop = asyncio.get_event_loop()
  with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:   # 需要按此处方式进行设置，不然会报错
    loop.set_default_executor(executor)  # 设置默认的 executor
    coro = downloader_coro(cc_list, base_url, verbose, concur_req)
    counts = loop.run_until_complete(coro)
  loop.close()
  return counts


# 用新定义的函数替换相关模块中的函数
sys.modules['ch18.flags2_asyncio'].download_one = download_one


if __name__ == '__main__':
  main(download_many, DEFAULT_CONCUR_REQ, MAX_CONCUR_REQ)
