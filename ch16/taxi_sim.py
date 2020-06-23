"""
出租车仿真程序
"""

import random
import collections
import queue
import argparse
import time

DEFAULT_NUMBER_OF_TAXIS = 3 
DEFAULT_END_TIME = 180
SEARCH_DURATION = 5
TRIP_DURATION = 20
DEPATURE_INTERVAL = 5

Event = collections.namedtuple('Event', 'time proc action')


# BEGIN TAXI_PROCESS
def taxi_process(ident, trips, start_time=0):
  """
  每次改变状态时创建事件，把控制权让给仿真器

  通过 time 将多个事件串联起来
  """
  time = yield Event(start_time, ident, 'leave garage')  
  for i in range(trips):
    time = yield Event(time, ident, 'pick up passenger')  # 产生 Event 实例，表示拉到乘客。协程会在这里暂停，等待主循环发送时间
    time = yield Event(time, ident, 'drop off passenger')  # 产生 Event 实例，表示乘客下车。协程会在这里暂停，等待主循环发送时间

  yield Event(time, ident, 'going home')
  # 出租车进程结束
# END TAXI_PROCESS


# BEGIN TAXI_SIMULATOR
class Simulator:

  def __init__(self, procs_map):
    self.events = queue.PriorityQueue()  # 保存排定事件的 PriorityQueue 对象（会按对象的第一个属性值进行排序），按时间正向排序
    self.procs = dict(procs_map)  # 避免在仿真的过程中，修改传入的参数

  def run(self, end_time):
    """
    排定并显示事件，直到时间结束
    """
    # 排定出租车的第一个事件
    for _, proc in sorted(self.procs.items()):  # 获取按键排序的元素
      first_event = next(proc)  # 预激协程，并接收产生的第一个 Event 对象
      self.events.put(first_event)  # 将各个对像添回到 PriorityQueue 对象中

    # 仿真系统的主循环
    sim_time = 0
    while sim_time < end_time:
      if self.events.empty():
        print('*** end of events ***')
        break

      current_event = self.events.get()  # 获取优先队列中 time 属性最小的 Event 对象
      sim_time, proc_id, previous_action = current_event
      print('taxi:', proc_id, proc_id * '\t', current_event)
      active_proc = self.procs[proc_id]  # 从字典中获取当前活动的出租车的协程
      next_time = sim_time + compute_duration(previous_action)  # 传入前一个动作，将结果加到 sim_time 上，计算出下一次活动的时间
      try:
        next_event = active_proc.send(next_time)
      except StopIteration:
        del self.procs[proc_id]  # 从字典中删除相应的协程
      else:
        self.events.put(next_event)  # 否则将 next_event 放入队列中
    else:  # 如果循环由于仿真时间到了而退出，显示待完成的事件数量
      msg = '*** end of simulation time: {} events pending ***'
      print(msg.format(self.events.qsize()))
# END TAXI_SIMULATOR


def compute_duration(previous_action):
    """
    使用指数分布计算操作的耗时
    """
    if previous_action in ['leave garage', 'drop off passenger']:
        # 新状态是四处排佪
        interval = SEARCH_DURATION
    elif previous_action == 'pick up passenger':
        # 新状态是行程开始
        interval = TRIP_DURATION
    elif previous_action == 'going home':
        interval = 1
    else:
        raise ValueError('Unknown previous_action: %s' % previous_action)
    return int(random.expovariate(1/interval)) + 1
        

def main(end_time=DEFAULT_END_TIME, num_taxis=DEFAULT_NUMBER_OF_TAXIS, seed=None):
    """
    初始化随机生成器，构建过程，运行仿真程序
    """
    if seed is not None:
        random.seed(seed)  # 获取可复现的结果

    taxis = {i: taxi_process(i, (i+1)*2, i*DEPATURE_INTERVAL) for i in range(num_taxis)}
    sim = Simulator(taxis)
    sim.run(end_time)

    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Taxi fleet simulator')
    parser.add_argument('-e', '--end-time', type=int, 
                        default=DEFAULT_END_TIME,
                        help='simulation end time; default =%s' % DEFAULT_END_TIME)
    parser.add_argument('-t', '--taxis', type=int, 
                        default=DEFAULT_NUMBER_OF_TAXIS, 
                        help='number of taxis running; defalut=%s' % DEFAULT_NUMBER_OF_TAXIS)
    parser.add_argument('-s', '--seed', type=int, default=None,
                        help='random generator seed (for testing)')
    
    args = parser.parse_args()
    main(args.end_time, args.taxis, args.seed)