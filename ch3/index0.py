"""创建从一个单词到其出现情况的映射"""

import sys
import re

WORD_RE = re.compile(r'\w+')

index = {}
with open(sys.argv[1]) as fp:
  for line_no, line in enumerate(fp, 1):
    for match in WORD_RE.finditer(line):
      word = match.group()
      column_no = match.start() + 1
      location = (line_no, column_no)
      occurences = index.get(word, [])  # get 只会在当值不存在时，返回默认值
      occurences.append(location)  
      index[word] = occurences  # 应对值不存在的情况，又涉及一次查询

# 以字母序打印输出结果
for word in sorted(index, key=str.upper):
  print(word, index[word])