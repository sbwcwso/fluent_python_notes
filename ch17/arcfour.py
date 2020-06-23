"""兼容 RC4 的算法"""


def arcfour(key, in_bytes, loops=20):

  kbox = bytearray(256)  # 创建储存键的数组
  for i, car in enumerate(key):  # 复制键和向量
    kbox[i] = car
  j = len(key)
  for i in range(j, 256):  # 重复到底
    kbox[i] = kbox[i-j]

  # [1] 初始化 sbox
  sbox = bytearray(range(256))

  # 按照 CipherSaber -2 的建议，不断打乱 sbox
  # http://ciphersaber.gurus.com/faq.html#cs2
  j = 0
  for k in range(loops):
    for i in range(256):
      j = (j + sbox[i] + kbox[i]) % 256
      sbox[i], sbox[j] = sbox[j], sbox[i]

  # 主循环
  i = 0
  j = 0
  out_bytes = bytearray()

  for car in in_bytes:
    i = (i + 1) % 256
    # [2] 打乱 sbox
    j = (j + sbox[i])  % 256
    sbox[i], sbox[j] = sbox[j], sbox[i]
    # [3] 计算 t
    t = (sbox[i] + sbox[j]) % 256
    k = sbox[t]
    car ^= k
    out_bytes.append(car)

  return out_bytes


def test():
  from time import time
  clear = bytearray(b'1234567890' * 100000)
  t0 = time()
  cipher = arcfour(b'key', clear)
  print('elapse time: %.2fs' % (time() - t0))
  result = arcfour(b'key', cipher)
  assert result == clear, '%r != %r' % (result, clear)
  print('elapsed time: %.2fs' % (time() - t0) )
  print('OK')


if __name__ == '__main__':
  test()
