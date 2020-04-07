"""示例 7-19　使用缓存实现，速度更快"""

import functools
from ch7.clockdeco2 import clock


@functools.lru_cache()  # 加括号的原因是 lur_cache 可以接受配置参数
@clock
def fibonacci(n):
  return n if n < 2 else fibonacci(n-2) + fibonacci(n-1)


if __name__ == "__main__":
  print(fibonacci(6))