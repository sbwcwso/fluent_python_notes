def make_averager():
  """示例 7-9　average.py：计算移动平均值的高阶函数"""
  series = []

  def averager(new_value):
    series.append(new_value)
    total = sum(series) 
    return total / len(series)

  return averager