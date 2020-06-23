import re
import reprlib

RE_WORD = re.compile('\w+')


class Sentence:
  def __init__(self, text):
    self.text = text

  def __repr__(self):
    return 'Sentence(%s)' % reprlib.repr(self.text)

  def __iter__(self):
    for match in RE_WORD.finditer(self.text):
      yield match.group()  # match.group() 方法从 MatchObject 实例中提取匹配正则表达式的具体文本