from collections import abc
import keyword


class FrozenJSON:
  """
  一个只读接口，使用属性表示法访问 JSON 类对象
  """

  def __new__(cls, arg):  # __new__ 是类方法,第一个参数是类本身,余下的参数与 __init__ 方法一样,只不过没有 self
    if isinstance(arg, abc.Mapping):
      return super().__new__(cls)  # 默认的行为是委托给超类的 __new__ 方法。这里调用的是 object 基类的 __new__ 方法,把唯一的参数设为 FrozenJSON
    elif isinstance(arg, abc.MutableSequence): 
      return [cls(item) for item in arg]
    else:  # 如果既不是字典也不是列表,那么原封不动地返回元素
      return arg

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
      return FrozenJSON(self.__data[name])  # 否则,从 self.__data 中获取 name 键对应的元素,返回调用 FrozenJSON.build() 方法得到的结果