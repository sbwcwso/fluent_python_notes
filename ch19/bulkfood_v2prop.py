def quantity(storage_name):  # ➊ storage_name 参数确定各个特性的数据存储在哪儿;对 weight 特性来说,存储的名称是 'weight'
  def qty_getter(instance):  # ➋ qty_getter 函数的第一个参数可以命名为 self, 因为 qty_getter 函数不在类定义体中, 所以将其命名为 instance;instance 指代要把属性存储其中的 LineItem 实例
    return instance.__dict__[storage_name]  # ➌ qty_getter 引用了 storage_name,把它保存在这个函数的闭包里;值直接从 instance.__dict__ 中获取,为的是跳过特性,防止无限递归

  def qty_setter(instance, value):  # ➍ 定义 qty_setter 函数,第一个参数也是 instance
    if value > 0:
      instance.__dict__[storage_name] = value  # ➎ 值直接存到 instance.__dict__ 中,这也是为了跳过特性
    else:
      raise ValueError('value must be > 0')

  return property(qty_getter, qty_setter)


class LineItem:
  weight = quantity('weight')  # ➊ 使用工厂函数把第一个自定义的特性 weight 定义为类属性
  price = quantity('price')  # ➋ 第二次调用,构建另一个自定义的特性,price

  def __init__(self, description, weight, price):
    self.description = description
    self.weight = weight  # ➌ 这里,特性已经激活,确保不能把 weight 设为负数或零
    self.price = price
    
  def subtotal(self):
    return self.weight * self.price  # ➍ 这里也用到了特性,使用特性获取实例中存储的值