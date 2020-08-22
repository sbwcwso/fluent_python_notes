class Quantity:  # ➊ 描述符基于协议实现,无需创建子类
  def __init__(self, storage_name):
    self.storage_name = storage_name  # ➋ storage_name 属性是托管实例中存储值的属性的名称

  def __set__(self, instance, value):  # ➌ 尝试为托管属性赋值时,会调用 __set__ 方法; self 是描述符实例, 也是托管类的类属性; instance 是托管实例(LineItem 实例),value 是要设定的值
    if value > 0:
      instance.__dict__[self.storage_name] = value  # ➍ 必须直接处理托管实例的 __dict__ 属性;如果使用内置的 setattr 函数,会再次触发 __set__ 方法,导致无限递归. 因为托管属性和实际属性的名称相同
    else:
      raise ValueError('value must be > 0') 


class LineItem:
  weight = Quantity('weight')  # ➎ 第一个描述符实例绑定给 weight 属性
  price = Quantity('price')  # ➏ 第二个描述符实例绑定给 price 属性

  def __init__(self, description, weight, price):
    self.description = description
    self.weight = weight
    self.price = price

  def subtotal(self):
    return self.weight * self.price