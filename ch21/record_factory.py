def record_factory(cls_name, field_names):
  try:
    field_names = field_names.replace(',', ' ').split()  # ❶ 这里体现了鸭子类型:尝试在逗号或空格处拆分 field_names;如果失败,那么假定 field_names 本就是可迭代的对象, 一个元素对应一个属性名
  except AttributeError: # 不能调用.replace或.split方法
    pass # 假定field_names本就是标识符组成的序列
  field_names = tuple(field_names)  # ➋ 使用属性名构建元组,这将成为新建类的 __slots__ 属性; 此外, 这么做还设定了拆包和字符串表示形式中各字段的顺序

  def __init__(self, *args, **kwargs):  # ➌ 新建类的 __init__ 方法
    attrs = dict(zip(self.__slots__, args))
    attrs.update(kwargs)
    for name, value in attrs.items():
      setattr(self, name, value)

  def __iter__(self):  # ➍ 实现 __iter__ 函数,把类的实例变成可迭代的对象;按照__slots__ 设定的顺序产出字段值
    for name in self.__slots__: 
      yield getattr(self, name)

  def __repr__(self):  # ➎ 迭代 __slots__ 和 self, 生成友好的字符串表示形式
    values = ', '.join('{}={!r}'.format(*i) for i
    in zip(self.__slots__, self))
    return '{}({})'.format(self.__class__.__name__, values)
  
  cls_attrs = dict( __slots__ = field_names,  # ➏ 组建类属性字典
                    __init__ = __init__,
                    __iter__ = __iter__,
                    __repr__ = __repr__)
  
  return type(cls_name, (object,), cls_attrs)  # ➐ 调用 type 构造方法,构建新类,然后将其返回