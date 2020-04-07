"""示例 7-18　生成第 n 个斐波纳契数，递归方式非常耗时"""

from ch7.clockdeco2 import clock


@clock
def fibonacci(n):
  return n if n < 2 else fibonacci(n-2) + fibonacci(n-1)


if __name__ == "__main__":
  print(fibonacci(6))