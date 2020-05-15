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

  shortcut_names = 'xyzt'
  
  def __getattr__(self, name):
    cls = type(self)
    if len(name) == 1:
      pos = cls.shortcut_names.find(name)  # find 也会查找 yz， 但是前一句已经限定 name 中只能有一个字符
      if 0 <= pos < len(self._components):
        return self._components[pos]
    msg = '{.__name__!r} object has no attribute {!r}'
    raise AttributeError(msg.format(cls, name))

  def __setattr__(self, name, value):
    cls = type(self)
    if len(name) == 1:
      if name in cls.shortcut_names:  # 如果 name 是 xyzt 中的一个，设置特殊的错误消息
        error = 'readonly attribute {attr_name!r}'
      elif name.islower():  # 为所有的小写字母设置特殊的错误消息
        error = "can't set attributes 'a' to 'z' in {cls_name!r}"
      else:
        error = ''
  
      if error:
        msg = error.format(cls_name=cls.__name__, attr_name=name)
        raise AttributeError(msg)
    super().__setattr__(name, value)  # 在超类上调用 __setattr__ 方法，提供标准行为
  