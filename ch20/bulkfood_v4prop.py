def quantity():  # ➊ 没有 storage_name 参数
  try:
    quantity.counter += 1  # ➋ 为了在多次调用之间共享 counter,因此把它定义为 quantity 函数自身的属性
  except AttributeError:
    quantity.counter = 0  # ➌ 如果 quantity.counter 属性未定义,把值设为 0
  storage_name = '_{}:{}'.format('quantity', quantity.counter)  # ➍ 创建一个局部变量 storage_name,借助闭包保持它的值,供后面的 qty_getter 和 qty_setter 函数使用

  def qty_getter(instance):  # ➎ 使用内置的 getattr 和 setattr 函数实现相关功能
    return getattr(instance, storage_name)

  def qty_setter(instance, value):
    if value > 0:
      setattr(instance, storage_name, value)
    else:
      raise ValueError('value must be > 0')
  
  return property(qty_getter, qty_setter)


class LineItem:
  weight = quantity()
  price = quantity()

  def __init__(self, description, weight, price):
    self.description = description
    self.weight = weight
    self.price = price

  def subtotal(self):
    return self.weight * self.pric