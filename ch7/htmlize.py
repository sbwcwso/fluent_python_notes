"""示例 7-21　singledispatch 创建一个自定义的 htmlize.register 装饰器，把多个函数绑在一起组成一个泛函数"""

from functools import singledispatch
from collections import abc
import numbers
import html


@singledispatch
def htmlize(obj):
  content = html.escape(repr(obj))
  return '<pre>{}</pre>'.format(content)


@htmlize.register(str)
def _(text):
  content = html.escape(text).replace('\n', '<br>\n')
  return '<p>{0}</p>'.format(content)


@htmlize.register(numbers.Integral)  # numbers.Inergal 是 int 的虛拟超类
def _(n):
  return '<pre>{0} (0x{0:x})</pre>'.format(n)


@htmlize.register(tuple)
@htmlize.register(abc.MutableSequence)  # 叠放多个 register 装饰器， 让同一个函数支持不同类型
def _(seq):
  inner = '</li>\n<li>'.join(htmlize(item) for item in seq)
  return '<ul>\n<li>' + inner + '</li>\n</ul>'