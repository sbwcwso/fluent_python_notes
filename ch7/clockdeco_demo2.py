"""示例 7-26　clockdeco_param_demo1.py"""

import time
from ch7.clockdeco_param import clock


@clock('{name}({args}) dt={elapsed}s')
def snooze(seconds):
  time.sleep(seconds)


for i in range(3):
  snooze(.123)