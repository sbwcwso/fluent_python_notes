class HauntedBus:
  """备受幽灵乘客折磨的校车"""

  def __init__(self, passengers=[]):
    self.passengers = passengers

  def pick(self, name):
    self.passengers.append(name)

  def drop(self, name):
    self.passengers.remove(name)