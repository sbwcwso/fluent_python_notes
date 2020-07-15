
import asyncio
import concurrent
import os
import sys

import aiohttp
from aiohttp import web

from ch17.flags2_common import main, HTTPStatus, Result, save_flag
from ch18.flags2_asyncio import FetchError, downloader_coro, DEFAULT_CONCUR_REQ, MAX_CONCUR_REQ
from ch18.flags2_asyncio_executor import download_many

DEST_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)),'downloads/')


async def http_get(session, url):
  async with session.get(url) as resp:
    if resp.status == 200:
      ctype = resp.headers.get('Content-type', '').lower()
      if 'json' in ctype or url.endswith('json'):
        data = await resp.json()  # 在响应上调用 .json() 方法，解析响应，返回一个 Python 数据结构 －－ 这里是一个字典
      else:
        data = await resp.read()  # 读取原始字节
      return data
    elif resp.status == 404:
      raise web.HTTPNotFound()
    else:
      resp.raise_for_status()



async def get_country(session, base_url, cc):
  url = '{}/{cc}/metadata.json'.format(base_url, cc=cc.lower())
  metadata = await http_get(session, url)
  return metadata['country']


async def get_flag(session, base_url, cc):
  url = '{}/{cc}/{cc}.gif'.format(base_url, cc=cc.lower())
  return await http_get(session, url)


async def download_one(session, cc, base_url, semaphore, verbose):
  try:
    async with semaphore:
      image = await get_flag(session, base_url, cc)
    async with semaphore:
      country = await get_country(session, base_url, cc)
  except web.HTTPNotFound:
    status = HTTPStatus.not_found
    msg = 'not found'
  except Exception as exc:
    raise FetchError(cc) from exc
  else:
    country = country.replace(' ', '_')
    filename = '{}-{}.gif'.format(country, cc)
    loop = asyncio.get_event_loop()
    loop.run_in_executor(None, save_flag, image, filename, DEST_DIR)
    status = HTTPStatus.ok
    msg = 'OK'

  if verbose and msg:
    print(cc, msg)

  return Result(status, cc)


# 用新定义的函数替换相关模块中的函数
sys.modules['ch18.flags2_asyncio'].download_one = download_one


if __name__ == '__main__':
  main(download_many, DEFAULT_CONCUR_REQ, MAX_CONCUR_REQ)
