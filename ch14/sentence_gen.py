import re
import reprlib

RE_WORD = re.compile('\w+')


class Sentence:
  def __init__(self, text):
    self.text = text
    self.words = RE_WORD.findall(text)

  def __repr__(self):
    return 'Sentence(%s)' % reprlib.repr(self.text)

  def __iter__(self):
    for word in self.words:
      yield word
    return # 不是必须的，不管有没有 return 语句，生成器函数都不会抛出 StopIteration 异常，而是在生成完全部值后直接退出
    