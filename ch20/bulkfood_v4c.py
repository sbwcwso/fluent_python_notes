import ch20.model_v4c as model


class LineItem:
  weight = model.Quantity()
  price = model.Quantity()

  def __init__(self, description, weight, price):
    self.description = description
    self.weight = weight
    self.price = price

  def subtotal(self):
    return self.weight * self.price