import re

re_numbers_str = re.compile(r'\d+')  # 字符串类型
re_words_str = re.compile(r'\w+')  # 字符串类型
re_numbers_bytes = re.compile(rb'\d+')  # 字节类型
re_words_bytes = re.compile(rb'\w+')  #　字节类型

text_str = ("Ramanujan saw \u0be7\u0bed\u0be8\u0bef"  # 要搜索的 Unicode 文本，包括 1729 的泰米尔数字（逻辑行直到右括号才结束
        " as 1729 = 1³ + 12³ = 9³ + 10³.")  # 这个字符串在编译时与前一个拼接起来

text_bytes = text_str.encode('utf_8')  # 字节序列只能用字节序列正则表达式搜索

print('Text', repr(text_str), sep='\n  ')  
print('Numbers')
print('  str  :', re_numbers_str.findall(text_str))  # 字符串模式 r'\d+' 能匹配泰米尔数字和 ASCII 数字
print('  bytes:', re_numbers_bytes.findall(text_bytes))  # 字节序列模式 rb'\d+' 只能匹配 ASCII 字节中的数字
print('Words')
print('  str  :', re_words_str.findall(text_str))  # 字符串模式 r'\w+' 能匹配字母、上标、泰米尔数字和 ASCII 数字
print('  bytes:', re_words_bytes.findall(text_bytes))  # 字节序列模式 rb'\w+' 只能匹配 ASCII 字节中的字母和数字