"""
A two-dimensional vector class
"""

from array import array
import math


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
    
  def __str__(self):
    return str(tuple(self))  # 利用 Vector2d 是可迭代对象

  def __bytes__(self):
    return (bytes([ord(self.typecode)]) + 
        bytes(array(self.typecode, self)))

  def __eq__(self, other):
    return tuple(self) == tuple(other)

  def __hash__(self):
    return hash(self.x) ^ hash(self.y)

  def __abs__(self):
    return math.hypot(self.x, self.y)

  def __bool__(self):
    return bool(abs(self))

  def angle(self):
    return math.atan2(self.y, self.x)

  def __format__(self, fmt_spec=''):
    if fmt_spec.endswith('p'):  # 如果格式代码以 'p' 结尾，使用极坐标
      fmt_spec = fmt_spec[:-1]
      coords = (abs(self), self.angle())  # 构造一个元组，表示极坐标
      outer_fmt = '<{}, {}>'
    else:
      coords = self
      outer_fmt = '({}, {})'
    components = (format(c, fmt_spec) for c in coords)
    return outer_fmt.format(*components)
  
  @classmethod
  def frombytes(cls, octets):
    typecode = chr(octets[0])
    memv = memoryview(octets[1:]).cast(typecode)
    return cls(*memv)