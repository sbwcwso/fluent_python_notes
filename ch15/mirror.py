class LookingGlass:

  def __enter__(self):
    import sys
    self.original_write = sys.stdout.write
    sys.stdout.write = self.reverse_write
    return 'JABBERWOCKY'  # 存入到目标变量 what 中

  def reverse_write(self, text):
    self.original_write(text[::-1])

  def __exit__(self, exc_type, exc_value, traceback):
    import sys 
    sys.stdout.write = self.original_write  # 还原为原来的输入方法
    if exc_type is ZeroDivisionError:
      print('Please DO NOT divide by zero!')
    return True 