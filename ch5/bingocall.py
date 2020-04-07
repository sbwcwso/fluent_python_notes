import random

class BingoCage:
  def __init__(self, items):
    self._items = list(items)  # 在本地创建一个副本，防止列表参数的意外副作用
    random.shuffle(self._items)

  def pick(self):
    try:
      return self._items.pop()
    except IndexError:
      raise LookupError('pick from empty BingoCage')

  def __call__(self):
    return self.pick()