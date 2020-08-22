class Quantity:
  __counter = 0  # ➊ __counter 是 Quantity 类的类属性,统计 Quantity 实例的数量
  def __init__(self):
    cls = self.__class__  # ➋ cls 是 Quantity 类的引用
    prefix = cls.__name__
    index = cls.__counter
    self.storage_name = '_{}#{}'.format(prefix, index)  # ➌ 每个描述符实例的 storage_name 属性都是独一无二的,因为其值由描述符类的名称和 __counter 属性的当前值构成(例如,_Quantity#0) 
    cls.__counter += 1  # ➍ 递增 __counter 属性的值

  def __get__(self, instance, owner):  # ➎ 需要要实现 __get__ 方法,因为托管属性的名称与 storage_name 不同
    return getattr(instance, self.storage_name)  # ➏ 使用内置的 getattr 函数从 instance 中获取储存属性的值

  def __set__(self, instance, value):
    if value > 0:
      setattr(instance, self.storage_name, value)  # ➐ 使用内置的 setattr 函数把值存储在 instance 中
    else:
      raise ValueError('value must be > 0')


class LineItem:
  weight = Quantity()  # ➑ 不用再把托管属性的名称传给 Quantity 构造方法
  price = Quantity()

  def __init__(self, description, weight, price):
    self.description = description
    self.weight = weight
    self.price = price

  def subtotal(self):
    return self.weight * self.price