from collections import namedtuple

Result = namedtuple('Result', 'count averaage')

def averager():
  total = 0.0
  count = 0
  average = None
  while True:
    term = yield
    if term is None:
      break  # 只有协程正常退出，才能返回值
    total += term
    count += 1
    average = total / count
  return Result(count ,average)