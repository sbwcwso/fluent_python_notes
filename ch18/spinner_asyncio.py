import asyncio
import itertools
import sys


async def spin(msg):  # 使用 async 和 await 代替 @async.coroutine 和 yield from
  write, flush = sys.stdout.write, sys.stdout.flush
  for char in itertools.cycle('|/-\\'):
    status = char + ' ' + msg
    write(status)
    flush()
    write('\x08' * len(status))
    try:
      await asyncio.sleep(.1)  # 如此休眠不会阻塞事件循环
    except asyncio.CancelledError:  # 如果抛出此错误，说明发出了取消请求，需退出循环
      break
  write(' ' * len(status) + '\x08' * len(status))


async def slow_function():
  """
  假装等待　I/O 一段时间
  """
  await asyncio.sleep(3)  # 把控制权交给主循环，在休眠结束后恢复这个协程
  return 42


async def supervisor():
  spinner = asyncio.Task(spin('thinking!'))  # 排定　spin 的运行时间，使用一个　Task　对象包装　spin　协程，并立即返回
  print('spinner object: ', spinner)  # 显示　Task 对象
  result = await slow_function()
  spinner.cancel()  #　Task 对象可以取消;取消后会在协程当前暂停的 yield 处抛出　asyncio.CancelledError 异常。协程可以捕获这个异常,也可以延迟取消,甚至拒绝取消
  return result


def main():
  loop = asyncio.get_event_loop()  # 获取事件的循环引用
  result = loop.run_until_complete(supervisor())  # 驱动　supervisor 协程，让其运行完毕
  loop.close()
  print('Answer: ', result)


if __name__ == '__main__':
  main()
