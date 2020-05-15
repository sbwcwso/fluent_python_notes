class Vector2d:
  typecode = 'd'

  def __init__(self, x, y):
    self.__x = float(x)  # 使用两个前导下划线，将属性标记为私有的
    self.__y = float(y)

  @property  # 将读值方法标记为特性
  def x(self):
    return self.__x

  @property
  def y(self):
    return self.__y

  def __iter__(self):
    return(i for i in (self.x, self.y))  # 读取x, y 分量的方法保持不变

  def __repr__(self):
    class_name = type(self).__name__
    return '{}({!r}, {!r})'.format(class_name, *self)  # 由于 Vector2d 是可迭代对象， 因此 *self 会将 x 和 y 分量提供给 format 函数

  def __hash__(self):
    return hash(self.x) ^ hash(self.y)