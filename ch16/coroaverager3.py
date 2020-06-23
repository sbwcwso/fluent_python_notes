from collections import namedtuple
from inspect import getgeneratorstate
from coroutil import coroutine

Result = namedtuple('Result', 'count average')


# 子生成器
def averager():
  total = 0
  count = 0
  average = None
  while True:
    term = yield  # main 中发送的各个值绑定到 term 变量上
    if term is None: # 终止条件
      break
    total += term
    count += 1
    average = total / count
  return Result(count, average)


# 委派生成器
def grouper(results, key):
  while True:  # 每次迭代都会创建一个 averager 实例：每个实例都是作为协程使用的生成器对象
    results[key] = yield from averager()


# 客户端代码，即调用方
def main(data):
  results = {}
  for key, values in data.items():
    group = grouper(results, key)
    next(group)  # 预激 group 协程，激活的是委派生成器，子生成器会由 yield from 自动预激
    for value in values:  
      group.send(value)  # 把各个 value 传给 grouper。传入的值最终到达 averager 函数中 term = yield 那一行;grouper 永远不知道传入的值是什么
    group.send(None)  #! 重要  把 None 传入 grouper,导致当前的 averager 实例终止,也让 grouper 继续运行,再创建一个 averager 实例,处理下一组值
  report(results)


# 输出报告
def report(results):
  for key, result in sorted(results.items()):
    group, unit = key.split(';')
    print('{:2} {:5} averaging {:.2f}{}'.format(
        result.count, group, result.average, unit
    ))


data = {
  'girls;kg':
  [40.9, 38.5, 44.3, 42.2, 45.2, 41.7, 44.5, 38.0, 40.6, 44.5],
  'girls;m':
  [1.6, 1.51, 1.4, 1.3, 1.41, 1.39, 1.33, 1.46, 1.45, 1.43],
  'boys;kg':
  [39.0, 40.8, 43.2, 40.8, 43.1, 38.6, 41.4, 40.6, 36.3],
  'boys;m':
  [1.38, 1.5, 1.32, 1.25, 1.37, 1.48, 1.25, 1.49, 1.46],
}


if __name__ == '__main__':
  main(data)