import asyncio
import os
import time

import aiohttp  # 需要额外安装，因为其不在标准库中

from ch17.flags import BASE_URL, save_flag, show, POP20_CC

DEST_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)),'downloads/')


async def get_flag(session, cc):
  url = '{}/{cc}/{cc}.gif'.format(BASE_URL, cc=cc.lower())
  async with session.get(url) as resp: # 阻塞的操作通过协程实现，原书中的代码不再起作用，本处通过 session 客户端来解决
    return await resp.read()  # 读取响应内容是一条单独的异步操作


async def download_one(session, cc):
  image = await get_flag(session, cc)
  show(cc)
  # Python 在两个模块之间并不共享全局变量，需要以参数的形式传入
  save_flag(image, cc.lower() + '.gif', DEST_DIR)
  return cc


async def download_many(cc_list):
  async with aiohttp.ClientSession() as session:  # 参考：https://docs.aiohttp.org/en/stable/client_reference.html
    to_do = [download_one(session, cc) for cc in sorted(cc_list)]  # 构建一个生成器对象列表
    wait_coro = asyncio.wait(to_do)  # 一个协程，不是阻塞型函数，等待传给它的所有协程运行完毕后结束
    done, _ = await wait_coro
  return len(done)


def main():
  t0 = time.time()
  loop = asyncio.get_event_loop()  # 获取事件循环底层实现的引用
  count = loop.run_until_complete(download_many(POP20_CC))
  elapsed = time.time() - t0
  msg = '\n{} flags downloaded in {:.2f}s'
  print(msg.format(count, elapsed))


if __name__ == '__main__':
  main()
