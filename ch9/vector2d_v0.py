"""示例 9-2  vector2d_v0.py: 目前定义的都是特殊方法
"""

from array import array
import math


class Vector2d:
  typecode = 'd'

  def __init__(self, x, y):
    self.x = float(x)  # 使用 float 进行类型转换，尽量的捕获可能出现的错误
    self.y = float(y)

  def __iter__(self):
    return (i for i in (self.x, self.y))

  def __repr__(self):
    class_name = type(self).__name__
    return '{}({!r}, {!r})'.format(class_name, *self)  # 由于 Vector2d 是可迭代对象， 因此 *self 会将 x 和 y 分量提供给 format 函数

  def __str__(self):
    return str(tuple(self))  # 利用 Vector2d 是可迭代对象

  def __bytes__(self):
    return (bytes([ord(self.typecode)]) + 
        bytes(array(self.typecode, self)))

  def __eq__(self, other):
    return tuple(self) == tuple(other)

  def __abs__(self):
    return math.hypot(self.x, self.y)

  def __bool__(self):
    return bool(abs(self))