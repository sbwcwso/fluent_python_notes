import time


def clock(func):
  """示例 7-15　一个简单的装饰器，输出函数的运行时间"""
  def clocked(*args):  # 支持任意个定位参数
    t0 = time.perf_counter()
    result = func(*args)  # func 相当于自由变量
    elapsed = time.perf_counter() - t0
    name = func.__name__
    arg_str = ", ".join(repr(arg) for arg in args)
    print('[%0.8fs]%s(%s) -> %r' % (elapsed, name, arg_str, result))
    return result
  return clocked  # 返回内部函数，取低被装饰的函数