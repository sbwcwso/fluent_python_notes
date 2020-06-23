from concurrent import futures

from flags import save_flag, get_flag, show, main
from flags_threadpool import download_one

BASE_URL = 'http://localhost:8002/flags'


def download_many(cc_list):
  cc_list = cc_list[:5]
  with futures.ThreadPoolExecutor(max_workers=3) as executor:  
    to_do = []
    for cc in sorted(cc_list):
      future = executor.submit(download_one, cc)  # executor.submit 方法排定可调用对象的执行时间，然后返回一个 future，表示这个待执行的操作
      to_do.append(future)
      msg = 'Scheduled for {}:{}'
      print(msg.format(cc, future))  # 显示一个消息，包含国家代码和对应的 future
      
  results = []
  for future in futures.as_completed(to_do):  # 在 future 运行结束后产出 future
    res = future.result()
    msg = '{} result: {!r}'
    print(msg.format(future, res))
    results.append(res)

  return len(list(results))  # 返回获取的结果数量，如果有线程抛出异常，异常会在这里抛出


if __name__ == '__main__':
  main(download_many)
