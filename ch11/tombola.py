import abc


class Tombola(abc.ABC):

  @abc.abstractmethod
  def load(self, iterable):
    """从可迭代对象中添加元素"""

  @abc.abstractmethod
  def pick(self):
    """随机删除元素，然后将其返回
    
    如果实例为空，这个方法应该抛出 `LookupError`
    """

  def loaded(self):
    """如果至少有一个元素，返回 `True`， 否则返回 `False` """
    return bool(self.inspect())  # 抽象基类中的具体方法只能依赖抽象基类定义的接口

  def inspect(self):
    """返回一个有序数组，由当前元素构成"""
    items = []
    while True:
      try:
        items.append(self.pick())  # 由于不知道具体的子类如何储存元素，为了得到 inspect 的结果，可以不断调用 .pick 方法，将 Tombola 清空
      except LookupError:
        break
    self.load(items)  # 之后调用 .load(...) 把所有元素放回去
    return tuple(sorted(items))