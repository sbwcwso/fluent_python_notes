from collections import abc
import keyword


class FrozenJSON:
  """
  一个只读接口，使用属性表示法访问 JSON 类对象
  """
  def __init__(self, mapping):
    self.__data = {}
    for key, value in mapping.items():
      if keyword.iskeyword(key):
        key += '_'
      self.__data[key] = value

  def __getattr__(self, name):  # 仅当没有指定名称(name)的属性时才调用 __getattr__ 方法
    if hasattr(self.__data, name):  # 如果 name 是实例属性 __data 的属性,返回那个属性。调用 keys 等方法就是通过这种方式处理的
      return getattr(self.__data, name)
    else:
      return FrozenJSON.build(self.__data[name])  # 否则,从 self.__data 中获取 name 键对应的元素,返回调用 FrozenJSON.build() 方法得到的结果

  @classmethod
  def build(cls, obj):  # 一个备选构造方法,@classmethod 装饰器经常这么用
    if isinstance(obj, abc.Mapping):  # obj 是映射,那就构建一个 FrozenJSON 对象
      return cls(obj)
    elif isinstance(obj, abc.MutableSequence):  # 如果是 MutableSequence 对象,必然是列表, 因此,我们把 obj 中的每个元素递归地传给 .build() 方法,构建一个列表
      return [cls.build(item) for item in obj]
    else:  # 如果既不是字典也不是列表,那么原封不动地返回元素
      return obj