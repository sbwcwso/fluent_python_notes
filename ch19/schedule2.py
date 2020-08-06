import warnings
import inspect  # ➊ 在 load_db 函数中使用

import ch19.osconfeed as osconfeed

DB_NAME = 'ch19/data/schedule2_db'  # ➋ 因为要存储几个不同类的实例,所以我们要创建并使用不同的数据库文件
CONFERENCE = 'conference.115'


class Record:
  def __init__(self, **kwargs):
    self.__dict__.update(kwargs)

  def __eq__(self, other):  # ➌ __eq__ 方法对测试有重大帮助
    if isinstance(other, Record):
      return self.__dict__ == other.__dict__
    else:
      return NotImplemented

class MissingDatabaseError(RuntimeError):
  """需要数据库但没有指定数据库时抛出。"""  # ➊ 自定义的异常通常是标志类,没有定义体。写一个文档字符串,说明异常的用途,比只写一个 pass 语句要好。


class DbRecord(Record):  # ➋ 扩展 Record 类
  __db = None  # ➌ __db 类属性存储一个打开的 shelve.Shelf 数据库引用

  @staticmethod  # ➍ set_db 是静态方法,以此强调不管调用多少次,效果始终一样
  def set_db(db):
    DbRecord.__db = db  # ➎ 即使调用 Event.set_db(my_db),__db 属性仍在 DbRecord 类中设置

  @staticmethod  # ➏ get_db 也是静态方法,因为不管怎样调用,返回值始终是 DbRecord.__db 引用的对象
  def get_db():
    return DbRecord.__db
  
  @classmethod  # ➐ fetch 是类方法,因此在子类中易于定制它的行为
  def fetch(cls, ident):
    db = cls.get_db()
    try:
      return db[ident]  # ➑ 从数据库中获取 ident 键对应的记录
    except TypeError:
      if db is None:  # ➒ 抛出自定义的异常,说明必须设置数据库
        msg = "database not set; call '{}.set_db(my_db)'"
        raise MissingDatabaseError(msg.format(cls.__name__))
      else:  # ➓ 重新抛出 TypeError 异常,因为我们不知道怎么处理
        raise

  def __repr__(self):
    if hasattr(self, 'serial'):  # ⓫ 如果记录有 serial 属性,在字符串表示形式中使用
      cls_name = self.__class__.__name__
      return '<{} serial={!r}>'.format(cls_name, self.serial)
    else:
      return super().__repr__()  # ⓬ 调用继承的 __repr__ 方法

class Event(DbRecord):  # ➊ Event 类扩展 DbRecord 类

  @property
  def venue(self):
    key = 'venue.{}'.format(self.venue_serial)
    return self.__class__.fetch(key)  # ➋ 在 venue 特性中使用 venue_serial 属性构建 key,然后传给继承自 DbRecord 类的 fetch 类方法

  @property
  def speakers(self):
    if not hasattr(self, '_speaker_objs'):  # ➌ speakers 特性检查记录是否有 _speaker_objs 属性
      spkr_serials = self.__dict__['speakers']  # ➍ 如果没有,直接从 __dict__ 实例属性中获取 'speakers' 属性的值,防止无限递归,因为这个特性的公开名称也是 speakers
      fetch = self.__class__.fetch  # ➎ 获取 fetch 类方法的引用
      self._speaker_objs = [fetch('speaker.{}'.format(key))
                            for key in spkr_serials]   # ➏ 使用 fetch 获取 speaker 记录列表,然后赋值给 self._speaker_objs
    return self._speaker_objs  # ➐ 返回前面获取的列表

  def __repr__(self):
    if hasattr(self, 'name'):  # ➑ 如果记录有 name 属性,在字符串表示形式中使用
      cls_name = self.__class__.__name__
      return '<{} {!r}>'.format(cls_name, self.name)
    else:
      return super().__repr__()  # ➒ 否则,调用继承的 __repr__ 方法

def load_db(db):
  raw_data = osconfeed.load()
  warnings.warn('loading ' + DB_NAME)
  for collection, rec_list in raw_data['Schedule'].items():
    record_type = collection[:-1]  # ➊ 目前,与 schedule1.py 脚本(见示例 19-9)中的 load_db 函数一样
    cls_name = record_type.capitalize()  # ➋ 把 record_type 变量的值首字母变成大写(例如,把 'event' 变成 'Event'),获取可能的类名
    cls = globals().get(cls_name, DbRecord)  # ➌ 从模块的全局作用域中获取那个名称对应的对象;如果找不到对象,使用 DbRecord
    if inspect.isclass(cls) and issubclass(cls, DbRecord):  # ➍ 如果获取的对象是类,而且是 DbRecord 的子类
      factory = cls  # ➎ ......把对象赋值给 factory 变量。因此,factory 的值可能是 DbRecord 的任何一个子类,具体的类取决于 record_type 的值。
    else:
      factory = DbRecord  # ➏ 否则,把 DbRecord 赋值给 factory 变量
    for record in rec_list:  # ➐ 这个 for 循环创建 key,然后保存记录,这与之前一样
      key = '{}.{}'.format(record_type, record['serial'])
      record['serial'] = key
      db[key] = factory(**record)  # ➑ 存储在数据库中的对象由 factory 构建,factory 可能是 DbRecord 类,也可能是根据 record_type 的值确定的某个子类