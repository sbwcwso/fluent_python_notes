import warnings

import ch19.osconfeed as osconfeed

DB_NAME = 'ch19/data/schedule1_db'
CONFERENCE = 'conference.115'

class Record:
  def __init__(self, **kwargs):
    self.__dict__.update(kwargs) # ➋ 使用关键字参数传入的属性构建实例的常用简便方式

def load_db(db):
  raw_data = osconfeed.load()
  warnings.warn('loading ' + DB_NAME)
  for collection, rec_list in raw_data['Schedule'].items():
    record_type = collection[:-1] # ➎ record_type 的值是去掉尾部 's' 后的集合名(即把 'events' 变成 'event')
    for record in rec_list:
      key = '{}.{}'.format(record_type, record['serial']) # ➏ 使用 record_type 和 'serial' 字段构成 key。
      record['serial'] = key
      db[key] = Record(**record)  # ➑ 构建 Record 实例,存储在数据库中的 key 键名下