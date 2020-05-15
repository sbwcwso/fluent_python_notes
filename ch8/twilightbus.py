class TwilightBus:
  """让乘客销声匿迹的校车"""

  def __init__(self, passengers=None):
    self.passengers = [] if passengers is None else passengers

  def pick(self, name):
    self.passengers.append(name)

  def drop(self, name):
    self.passengers.remove(name)