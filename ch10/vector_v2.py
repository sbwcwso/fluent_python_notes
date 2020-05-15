from array import array
import reprlib
import math
import numbers


class Vector:
  typecode = 'd'

  def __init__(self, components):
    self._components = array(self.typecode, components)  # 受保护的属性

  def __iter__(self):
    return iter(self._components)

  def __repr__(self):
    components = reprlib.repr(self._components)  # 获取 self._components 的有限长度表示
    components = components[components.find('['):-1]  # 去掉前面的 array( 'd 和后面的的 )
    return 'Vector({})'.format(components)
  
  def __str__(self):
    return str(tuple(self))  # 利用 Vector2d 是可迭代对象

  def __bytes__(self):
    return (bytes([ord(self.typecode)]) + 
        bytes(array(self.typecode, self)))

  def __eq__(self, other):
    return tuple(self) == tuple(other)

  def __abs__(self):
    return math.sqrt(sum(x * x for x in self))

  def __bool__(self):
    return bool(abs(self))

  def angle(self):
    return math.atan2(self.y, self.x)

  @classmethod
  def frombytes(cls, octets):
    typecode = chr(octets[0])
    memv = memoryview(octets[1:]).cast(typecode)
    return cls(memv)

  def __len__(self):
    return len(self._components)

  def __getitem__(self, index):
    cls = type(self)  # 获取实例所属的类
    if isinstance(index, slice):
      return cls(self._components[index])
    elif isinstance(index, numbers.Integral):  # 如果 index 是 int 或其他整数类型
      return self._components[index]
    else:
      msg = '{cls.__name__} indices must be integers'
      raise TypeError(msg.format(cls=cls))