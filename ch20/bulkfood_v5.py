import ch20.model_v5 as model  # ➊ 导入 model_v5 模块,指定一个更友好的名称


class LineItem:
  description = model.NonBlank()  # ➋ 使用 model.NonBlank 描述符。其余的代码没变
  weight = model.Quantity()
  price = model.Quantity()

  def __init__(self, description, weight, price):
    self.description = description
    self.weight = weight
    self.price = price

  def subtotal(self):
    return self.weight * self.price