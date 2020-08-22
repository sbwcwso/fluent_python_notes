
class Quantity:
  __counter = 0

  def __init__(self):
    cls = self.__class__
    prefix = cls.__name__
    index = cls.__counter
    self.storage_name = '_{}#{}'.format(prefix, index)
    cls.__counter += 1

  def __get__(self, instance, owner):
    if instance is None:
      return self  # ➊ 如果不是通过实例调用,返回描述符自身
    else:
      return getattr(instance, self.storage_name)  # ➋ 否则,像之前一样,返回托管属性的值

  def __set__(self, instance, value):
    if value > 0:
      setattr(instance, self.storage_name, value)
    else:
      raise ValueError('value must be > 0')


class LineItem:
  weight = Quantity()
  price = Quantity()

  def __init__(self, description, weight, price):
    self.description = description
    self.weight = weight
    self.price = price

  def subtotal(self):
    return self.weight * self.price