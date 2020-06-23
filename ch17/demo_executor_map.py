from time import sleep, strftime
from concurrent import futures


def display(*args):
  """
  将传入的参数打印出来，并在前面加上 [HH:MM::SS] 格式的时间戳
  """
  print(strftime('[%H:%M:%S]'), end=' ')
  print(*args)


def loiter(n):
  """
  休眠并显示特定的消息
  """
  msg = '{}loiter({}): doing nothing for {} s...'
  display(msg.format('\t'*n, n, n))
  sleep(n)
  msg = '{}loiter({}): done.'
  display(msg.format('\t'*n, n))
  return n*10


def main():
  display('Script starting.')
  executor = futures.ThreadPoolExecutor(max_workers=3)
  results = executor.map(loiter, range(5))  # 非阻塞调用
  display('results:', results)
  display('Waiting for individual results:')
  for i, result in enumerate(results):
    display('result {}: {}'.format(i, result))


if __name__ == '__main__':
  main()
