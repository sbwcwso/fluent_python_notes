from concurrent import futures

from flags import save_flag, get_flag, show, main

MAX_WORKERS = 20  # 设定 ThreadPoolExecutor 类最多使用几个线程


def download_one(cc):
  """
  下载一个图像的函数，在各个线程中执行的函数
  """
  image = get_flag(cc)
  show(cc)
  save_flag(image, cc.lower() + '.gif')
  return cc


def download_many(cc_list):
  workers = min(MAX_WORKERS, len(cc_list))  # 设定允许的线程数量
  print('running')
  with futures.ThreadPoolExecutor(workers) as executor:  # excutor.__exit__ 方法会调用 executor.shutdown(wait=True) 方法，它会在所有线程都执行完毕前阻塞进程
    res = executor.map(download_one, sorted(cc_list))  # map 方法返回的是一个生成器，可以迭代，获取各个函数的返回值

  return len(list(res))  # 返回获取的结果数量，如果有线程抛出异常，异常会在这里抛出


if __name__ == '__main__':
  main(download_many)
