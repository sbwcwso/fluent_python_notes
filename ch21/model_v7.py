import abc


class AutoStorage:  # ➊ AutoStorage 类提供了之前 Quantity 描述符的大部分功能
  __counter = 0

  def __init__(self):
    cls = self.__class__
    prefix = cls.__name__
    index = cls.__counter
    self.storage_name = '_{}#{}'.format(prefix, index)
    cls.__counter += 1

  def __get__(self, instance, owner):
    if instance is None:
      return self
    else:
      return getattr(instance, self.storage_name)

  def __set__(self, instance, value):
      setattr(instance, self.storage_name, value)  # ➋ ......验证除外


class Validated(abc.ABC, AutoStorage):  # ➌ Validated 是抽象类,不过也继承自 AutoStorage 类
  def __set__(self, instance, value):
    value = self.validate(instance, value)  # ➍ __set__ 方法把验证操作委托给 validate 方法......
    super().__set__(instance, value)  # ➎ ......然后把返回的 value 传给超类的 __set__ 方法,存储值
    
  @abc.abstractmethod
  def validate(self, instance, value):  # ➏ validate 是类的抽象方法
    """return validated value or raise ValueError"""


class Quantity(Validated):  # ➐ Quantity 和 NonBlank 都继承自 Validated 类
  """a number greater than zero"""
  def validate(self, instance, value):
    if value <= 0:
      raise ValueError('value must be > 0')
    return value


class NonBlank(Validated):
  """a string with at least one non-space character"""
  def validate(self, instance, value):
    value = value.strip()
    if len(value) == 0:
      raise ValueError('value cannot be empty or blank')
    return value  # ➑ 要求具体的 validate 方法返回验证后的值,借机可以清理、转换或规范化接收的数据。这里把 value 首尾的空白去掉,然后将其返回


class EntityMeta(type):
  """元类,用于创建带有验证字段的业务实体"""
  def __init__(cls, name, bases, attr_dict):
    super().__init__(name, bases, attr_dict)  # 在超类(在这里是 type)上调用 __init__ 方法
    for key, attr in attr_dict.items():   # 与示例 21-4 中 @entity 装饰器的逻辑一样
      if isinstance(attr, Validated):
        type_name = type(attr).__name__
        attr.storage_name = '_{}#{}'.format(type_name, key)

class Entity(metaclass=EntityMeta):  # 这个类的存在只是为了用起来便利:这个模块的用户直接继承Entity 类即可,无需关心 EntityMeta 元类,甚至不用知道它的存在
  """带有验证字段的业务实体"""