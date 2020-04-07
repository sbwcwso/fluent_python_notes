"""创建从一个单词到其出现情况的映射"""

import sys
import re

WORD_RE = re.compile("\w+")

index = {}
with open(sys.argv[1]) as fp:
  for line_no, line in enumerate(fp, 1):
    for match in WORD_RE.finditer(line):
      word = match.group()
      column_no = match.start() + 1
      location = (line_no, column_no)
      index.setdefault(word, []).append(location) # 一次查询即可达到目的

# 以字母序打印出结果
for word in sorted(index, key=str.upper):
  print(word, index[word])
      