"""示例 7-25　clockdeco_param.py 模块：参数化 clock 装饰器"""

import time
import functools

DEFAULT_FMT = '[{elapsed:0.8f}s] {name}({args}) -> {result}'


def clock(fmt=DEFAULT_FMT):
  def decorate(func):
    @functools.wraps(func)
    def clocked(*args, **kwargs):
      t0 = time.time()
      _result = func(*args, **kwargs)
      elapsed = time.time() - t0
      name = func.__name__
      arg_lst = []
      if args:
        arg_lst.append(", ".join(repr(arg) for arg in args))
      if kwargs:
        pairs = ['%s=%r' % (k, w) for k, w in sorted(kwargs.items())]
        arg_lst.append(', '.join(pairs))
      args = ', '.join(arg_lst)
      result = repr(_result)  # 便于显示
      print(fmt.format(**locals()))  # 在 fmt 中引用 clocked 的局部变量
      return _result
    return clocked
  return decorate


if __name__ == "__main__":
  @clock()
  def snozze(seconds):
    time.sleep(seconds)

  for i in range(3):
    snozze(.123)