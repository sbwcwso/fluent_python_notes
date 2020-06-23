from functools import wraps

def coroutine(func):
  """
  装饰器：向前执行到第一个 yield 表达式，预激 func
  """
  @wraps(func)
  def primer(*args, **kwargs):
    gen = func(*args, **kwargs)
    next(gen)  # 预激生成器
    return gen  # 返回生成器
  return primer