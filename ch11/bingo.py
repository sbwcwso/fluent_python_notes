import random

from ch11.tombola import Tombola


class BingoCage(Tombola):
  def __init__(self, items):
    # 。random.SystemRandom 使用os.urandom(...) 函数实现 random API
    #根据 os 模块的文档，os.urandom(...)函数生成“适合用于加密”的随机字节序列。
    self._randomizer = random.SystemRandom()
    self._items = []
    self.load(items)

  def load(self, items):
    self._items.extend(items)
    self._randomizer.shuffle(self._items)

  def pick(self):
    try:
      return self._items.pop()     
    except IndexError:
      raise LookupError('pick form empty BingoCage')

  def __call__(self):
    self.pick()