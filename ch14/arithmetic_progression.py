class ArithmeticProgression:
  
  def __init__(self, begin, step, end=None):
    self.begin = begin
    self.step = step
    self.end = end  # None -> 无穷数列

  def __iter__(self):
    result = type(self.begin + self.step)(self.begin)  # 为了让数列的首项与其他项的类型一样，先做加法运算，然后使用计算结果的类型强制转换生成的结果
    forever = self.end is None
    index = 0
    while forever or result < self.end:
      yield result
      index += 1
      # 没有直接使用 self.step 不断地增加 result，而是选择使用 index 变量，
      # 把 self.begin 与 self.step 和 index 的乘积相加，计算 result 的各个值，
      # 以此降低处理浮点数时累积效应致错的风险。
      result = self.begin + self.step * index  