import collections
from concurrent import futures

import requests
import tqdm

from flags2_common import main, HTTPStatus
from flags2_sequential import download_one

DEFAULT_CONCUR_REQ = 30  # 默认并发请求数的最大值
MAX_CONCUR_REQ = 1000  # 限制最大的并发请求数，一项安全措施


def download_many(cc_list, base_url, verbose, concur_req):
  counter = collections.Counter()
  with futures.ThreadPoolExecutor(max_workers=concur_req) as executor:  # main 函数中会选取 concur_req:MAX_CONCUR_REQ, len(cc_list), -m/--max_req 命令行选项的值，如此，能避免创建超过所需的线程
    to_do_map = {}  # 把各个 Futute 实例（表示一次下载）映射到相应的国家代码上，在处理错误时使用
    for cc in sorted(cc_list):
      future = executor.submit(download_one, cc, base_url, verbose)  # 排定一个可调用对象的执行时间，然后返回一个 Future 实例。第一个参数是可调用对象，其余参数是传递给可调用对象的参数
      to_do_map[future] = cc
    done_iter = futures.as_completed(to_do_map)  # 返回迭代器，在 future 运行结束后产出 future
    if not verbose:
      done_iter = tqdm.tqdm(done_iter, total=len(cc_list))  # done_iter 没有 len 函数，需要通过 totoal 参数，借助 len(cc_list) 来指定
    for future in done_iter:
      try:
        res = future.result()  # 要么返回结果，要么抛出可调用对象在执行过程中抛出的异常。 在此示例中，不会发生阻塞，因为 as_completed 方法只返回已经运行结速的 future
      except requests.exceptions.HTTPError as exc:  # 处理 get_flag 函数抛出的与 HTTP 有关的且 download_one 没有处理的异常
        error_msg = 'HTTP error {res.status_code} - {res.reason}'
        error_msg = error_msg.format(res=exc.response)
      except requests.exceptions.ConnectionError as exc:
        error_msg = 'Connection error'
      else:
        error_msg = ''
        status = res.status

      if error_msg:
        status = HTTPStatus.error
      counter[status] += 1  # 以 HTTPStatus(一个 Enum) 中的值为键，增加计数器
      if verbose and error_msg:  # 如果是详细模式，则有错误，则显示带有当前国家代码的错误信息
        cc = to_do_map[future]  # 以当前 future 为键，从 to_do_map 中获取国家代码
        print('*** Error for {}:{}'.format(cc, error_msg))

  return counter


if __name__ == '__main__':
  main(download_many, DEFAULT_CONCUR_REQ, MAX_CONCUR_REQ)
