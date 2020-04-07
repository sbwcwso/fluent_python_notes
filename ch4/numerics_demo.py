import unicodedata
import re

re_digit = re.compile(r'\d')

sample = '1\xbc\xb2\u0969\u136b\u216b\u2466\u2480\u3285'

for char in sample:
  print('U+%04x' % ord(char),  # U+0000 格式的码位
     char.center(6),  # 在长度为 6 的字符串中居中显示
     're_dig' if re_digit.match(char) else '-',
     'isdig' if char.isdigit() else '-',
     'isnum' if char.isnumeric() else '-', 
     format(unicodedata.numeric(char), '5.2f'),
     unicodedata.name(char),
     sep='\t')