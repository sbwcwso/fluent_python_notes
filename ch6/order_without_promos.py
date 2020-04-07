"""示例 6-1"""


from abc import ABC, abstractmethod
from collections import namedtuple
import ch6.promotions as promotions
import inspect


Customer = namedtuple('Customer', 'name fidelity')


class LineItem:
  def __init__(self, product, quantity, price):
    self.product = product
    self.quantity = quantity
    self.price = price

  def total(self):
    return self.price * self.quantity


class Order:  # 上下文
  def __init__(self, customer, cart, promotation=None):
    self.customer = customer
    self.cart = list(cart)
    self.promotation = promotation

  def total(self):
    if not hasattr(self, '__total'):
      self.__total = sum(item.total() for item in self.cart)
    return self.__total

  def due(self):
    if self.promotation is None:
      discount = 0
    else:
      discount = self.promotation(self)
    return self.total() - discount
  
  def __repr__(self):
    fmt = '<Order total: {:.2f} due:{:.2f}>'
    return fmt.format(self.total(), self.due())


promos = [func for name, func in 
          inspect.getmembers(promotions, inspect.isfunction)]


def best_promo(order):
  """选择是佳的折扣策略
  """
  return max(promo(order) for promo in promos)