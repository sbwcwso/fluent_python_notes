import contextlib


@contextlib.contextmanager
def looking_glass():
  import sys
  original_write = sys.stdout.write

  def reverse_write(text):
    original_write(text[::-1])

  sys.stdout.write = reverse_write
  yield 'JABBEREOCKY'
  sys.stdout.write = original_write