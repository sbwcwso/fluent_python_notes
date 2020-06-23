import re
import reprlib

RE_WORD = re.compile('\w+')


class Sentence:
  def __init__(self, text):
    self.text = text
    self.words = RE_WORD.findall(text)  # 返回一个字符串列表，里面的元素是正则表达式的全部非重叠匹配
  
  def __getitem__(self, index):
    return self.words[index]

  def __len__(self):  # 为了完善序列协议，需要 __len__ 方法；但如果只是让对象可以迭代，没必要实现此方法
    return len(self.words)

  def __repr__(self):
    return 'Sentence(%s)' % reprlib.repr(self.text)  # 用于生成大型数据结构的简略字符串表示形式