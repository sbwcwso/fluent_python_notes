class Averager():
  """示例 7-8　average_oo.py：计算移动平均值的类
  """
  def __init__(self):
    self.series = []

  def __call__(self, new_value):
    self.series.append(new_value)
    return sum(self.series) / len(self.series)