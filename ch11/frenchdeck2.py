import collections

Card = collections.namedtuple('Card', ['rank', 'suit'])


class FrenchDeck2(collections.MutableSequence):
  ranks = [str(n) for n in range(2, 11)] + list('JQKA')
  suits = 'spades diamonds clubs hearts'.split()

  def __init__(self):
    self._cards = [Card(rank, suit) for suit in self.suits
                      for rank in self.ranks]

  def __len__(self):
    return len(self._cards)

  def __getitem__(self, position):
    return self._cards[position]

  def __setitem__(self, position, value):  # 为了支持洗牌，只需实现 __setitem__ 方法
    self._cards[position] = value

  def __delitem__(self, position):  # 继承 MutableSequence 的类必须实现 __delitem__ 方法
    del self._cards[positon]

  def insert(self, position, value):  # 继承 MutableSequence 的类必须实现 insert 方法
    self._cards.insert(position, value)