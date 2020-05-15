from random import randrange

from tombola import Tombola

@Tombola.register  # 把 Tombolist 注册为 Tombola 的虚拟子类
class TomboList(list):

  def pick(self):
    if self:  # Tombolist 从 list 中继承 __bool__ 方法，列表不为空时返回 True
      position = randrange(len(self))
      return self.pop(position)
    else:
      raise LookupError('pop from empty TomboList')
    
  load = list.extend  # Tombolist.load 与 list.extend 一样

  def loaded(self):
    return bool(self)

  def inspect(self):
    return tuple(sorted(self))