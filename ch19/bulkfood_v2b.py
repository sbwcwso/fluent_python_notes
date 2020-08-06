class LineItem:

  def __init__(self, description, weight, price):
    self.description = description
    self.weight = weight
    self.price = price
  
  def subtotal(self):
    return self.weight * self.price
  
  def get_weight(self):  # ➊ 普通的读值方法
    return self.__weight

  def set_weight(self, value):  # ➋ 普通的设值方法
    if value > 0:
      self.__weight = value
    else:
      raise ValueError('value must be > 0')

  weight = property(get_weight, set_weight)  # ➌ 构建 property 对象,然后赋值给公开的类属性