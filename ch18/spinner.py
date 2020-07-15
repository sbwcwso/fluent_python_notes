import itertools
import threading
import sys
import time


class Signal:
  """
  用于从外部控制协程
  """
  go = True


def spin(msg, signal):
  """
  在单独的线程中运行的函数
  """
  write, flush = sys.stdout.write, sys.stdout.flush
  for char in itertools.cycle('|/-\\'):  # 无限循环
    status = char + ' ' + msg
    write(status)
    flush()
    write('\x08' * len(status))  # 使用退格将光标移回之前的位置
    time.sleep(.1)
    if not signal.go:  # 如保 go 属性不再为 True，则退出循环
      break
  write(' ' * len(status) + '\x08' * len(status))  # 使用空格清除状态，将光标移回开头


def slow_function():
  """
  假设等待 IO 一段时间
  """
  time.sleep(3)
  return 42


def supervisor():
  """
  设置从属线程，显示线程对象，运行耗时计算，最后杀死线程
  """
  signal = Signal()
  spinner = threading.Thread(target=spin, args=('thinking!', signal))  # 设置从属线程
  print('spinner object:', spinner)  # 显示从属线程对象
  spinner.start()  # 启动从属线程
  result = slow_function()  # 阻塞主线程，从属线程以动画的形式显示旋转指针
  signal.go = False  # 改变 signal 的状态；此会终止 spin 函数中的 for 循环
  spinner.join()  # 等待 spinner 线程结束
  return result


def main():
  result = supervisor()
  print("Answer", result)


if __name__ == "__main__":
  main()
