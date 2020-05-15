import doctest

from tombola import Tombola

# 要测试的模块
import bingo, lotto, tombolist  # 导入真实子类和虚拟子类，用于测试
TEST_FILE = 'tombola_tests.rst'
TEST_MSG = '{0:16}{1.attempted:2} tests, {1.failed:2} failed - {2}'


def main(argv):
  verbose = '-v' in argv
  real_subclasses = Tombola.__subclasses__()  # __subclasses__() 返回的列表是内存中存在的直接子代
  virtual_subclasses = list(Tombola._abc_registry)

  for cls in real_subclasses + virtual_subclasses:
    test(cls, verbose)


def test(cls, verbose=False):

  res = doctest.testfile(
      TEST_FILE,
      globs={'ConcreteTombola': cls},
      verbose=verbose,
      optionflags=doctest.REPORT_ONLY_FIRST_FAILURE
  )
  tag = 'FAIL' if res.failed else 'OK'
  print(TEST_MSG.format(cls.__name__, res, tag))


if __name__ == "__main__":
  import sys
  main(sys.argv)