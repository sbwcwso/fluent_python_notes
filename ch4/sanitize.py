import unicodedata
import string


def shave_marks(txt):
  """去掉全部变音符号"""
  norm_txt = unicodedata.normalize('NFD', txt)
  shaved = ''.join(c for c in norm_txt if not unicodedata.combining(c))
  return unicodedata.normalize('NFC', shaved)


def shave_marks_latin(txt):
  """将拉打基字符中所有的变音符号删除"""
  norm_txt = unicodedata.normalize('NFD', txt)
  latin_base = False
  keepers = []
  for c in norm_txt:
    if unicodedata.combining(c) and latin_base:
      continue  # 怱略拉丁基字符上的变音符号
    keepers.append(c)
    if not unicodedata.combining(c):  # 如果不是组合字符，那就是新的基字符
      latin_base = c in string.ascii_letters
  shaved = ''.join(keepers)
  return unicodedata.normalize('NFC', shaved)


single_map = str.maketrans("""‚ƒ„†ˆ‹‘’“”•–—˜›""",
                """'f"*^<''""---~>""")

multi_map = str.maketrans({
    '€': '<euro>',
    '…': '...',
    'Œ': 'OE',
    '™': '(TM)',
    'œ': 'oe',
    '‰': '<per mille>',
    '‡': '**'
})

multi_map.update(single_map)


def dewinize(txt):
  """将 Win1252 符号替换成 ASCII 字符或序列"""
  return txt.translate(multi_map)


def asciize(txt):
  """调用 dewinize 函数，然后去掉变音符号"""
  no_marks = shave_marks_latin(dewinize(txt))
  no_marks = no_marks.replace('ß', 'ss')
  return unicodedata.normalize('NFKC', no_marks)