"""示例 7-23　为了接受参数，新的 register 装饰器必须作为函数调用"""

registry = set()


def register(active=True):
  def decorate(func):  # decorate 才是真正的装饰器，其接受一个函数作为参数
    print("running register(active=%s) -> decorate(%s)" %(active, func))
    if active:
      registry.add(func)
    else:
      registry.discard(func)  # 如果 active 为 false，且 func 在 registry 存在，则将其删除
    return func  # decorate 是装饰器，返回函数
  return decorate  # register 是装饰器工厂函数，返回装饰器


@register(active=False)  # @register 工厂函数必须作为函数调用，并且传入所需的参数
def f1():
  print('running f1()')


@register()
def f2():
  print('running f2()')


def f3():
  print('running f3()')