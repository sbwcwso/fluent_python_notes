"""示例 6-1"""


from abc import ABC, abstractmethod
from collections import namedtuple


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
      discount = self.promotation.discount(self)
    return self.total() - discount
  
  def __repr__(self):
    fmt = '<Order total: {:.2f} due:{:.2f}>'
    return fmt.format(self.total(), self.due())


class Promotation(ABC):  # 策略：抽象基类
  @abstractmethod
  def discount(self, order):
    """返回折扣金额（正值）"""
    pass


class FidelityPromo(Promotation):  # 第一个具体策略
  """为积分为 1000 或以上的顾客提供 5% 的折扣"""
  def discount(self, order):
    return order.total() * 0.05 if order.customer.fidelity > 1000 else 0


class BulkItemPromo(Promotation):  # 第二个策略
  """单个商品为 20 个或以上时，提供 10% 折扣"""
  def discount(self, order):
    discount = 0
    for item in order.cart:
      if item.quantity >= 20:
        discount += item.total() * 0.1
    return discount

class LargeOrderPromo(Promotation):  # 第三个策略
  """订单中的不同商品达到10个或以上时提供7%折扣"""
  def discount(self, order):
    distinct_items = {item.product for item in order.cart}
    return order.total() * 0.07 if len(distinct_items) >= 10 else 0