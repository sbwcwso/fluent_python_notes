class DemoException(Exception):
  """为这次演示定义的异常类型"""


def demo_exc_handling():
  print('-> coroutine started')
  while True:
    try:
      x = yield
    except DemoException:  # 特别处理 DemoException 异常
      print('*** DemoException handled. Continuing...')
    else:  # 如果没有异常，显示接收到的值
      print('-> coroutine received: {!r}'.format(x))
  raise RuntimeError('This line should never run.')  # 此行永远不会执行