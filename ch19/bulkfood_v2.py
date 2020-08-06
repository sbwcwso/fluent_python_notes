class LineItem:
  def __init__(self, description, weight, price):
    self.description = description
    self.weight = weight  # ➊ 使用特性的设值方法了,确保所创建实例的 weight 属性不能为负值
    self.price = price

  def subtotal(self):
    return self.weight * self.price

  @property  # ➋ @property 装饰读值方法
  def weight(self):  # ➌ 实现特性的方法,其名称都与公开属性的名称一样——weight
    return self.__weight  # ➍ 真正的值存储在私有属性 __weight 中

  @weight.setter  # ➎ 被装饰的读值方法有个 .setter 属性,这个属性也是装饰器;这个装饰器把读值方法和设值方法绑定在一起
  def weight(self, value):
    if value > 0:
      self.__weight = value  # ➏ 如果值大于零,设置私有属性 __weight
    else:
      raise ValueError('value must be > 0')  # ➐ 否则,抛出 ValueError 异常