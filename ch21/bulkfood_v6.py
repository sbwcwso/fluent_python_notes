import ch21.model_v6 as model

@model.entity  # ➊ 此类唯一的变化是添加了装饰器
class LineItem:
  description = model.NonBlank()
  weight = model.Quantity()
  price = model.Quantity()

  def __init__(self, description, weight, price):
    self.description = description
    self.weight = weight
    self.price = price
  
  def subtotal(self):
    return self.weight * self.price