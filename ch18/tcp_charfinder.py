import asyncio
import sys

from charfinder import UnicodeNameIndex  # 用于构建名称索引，提供查询方法

CRLF = b'\r\n'
PROMPT = b'?> '

index = UnicodeNameIndex()  # 实例化 UnicodeNameIndex 类时，会使用 charfinder_index.pickle 文件(如果存在)，或者构建这个文件，因此第一次运行时要等几秒钟服务器才会启动


async def handle_queries(reader, writer):  # 这个协程要传给 asyncio.start_server 函数，接收的两个参数是 asyncio.StreamReader 对象和 asyncio.StreamWriter 对象
  while True:  # 循环处理会话，直到从客户端接收到控制字符后退出
    writer.write(PROMPT)  # StreamWriter.write 方法不是协程，只是普通函数；这行代码发送 ?> 提示符
    await writer.drain()  # StreamWriter.drain 方法刷新 writer 缓冲，是协程
    data = await reader.readline()  # StreamReader.readline 方法是协程，返回一个 bytes 对象
    try:
      query = data.decode().strip()  # 默认编码 utf8
    except UnicodeDecodeError:
      query = '\x00'
    client = writer.get_extra_info('peername')  # 返回与套接子连接的远程地址
    print('Received from {}: {!r}'.format(client, query))  # 在服务器控制台中记录查询
    if query:
      if ord(query[:1]) < 32:
        break  # 如果收到控制字符或空字符，退出循环
      lines = list(index.find_description_strs(query))  # 返回一个生成器，产出包含 Unicode 码位、真正的字符串和字符名称的字符串，此处从生成器中构建了一个列表
      if lines:
        writer.writelines(line.encode() + CRLF for line in lines)  # 使用默认的 UTF-8 编码把 lines 转换为 bytes 对象，并在每一行添加回车符和换行符；此处的参数是一个生成器表达式
      writer.write(index.status(query, len(lines)).encode() + CRLF)  # 输出状态

      await writer.drain()  # 刷新输出缓存
      print('Sent {} results'.format(len(lines)))  #  在服务器控制台中记录响应

  print('Close the client socket')  # 在服务器的控制台中记录会话结束
  writer.close()  # 关闭 StreamWriter 流



def main(address='127.0.0.1', port=2323):
  port = int(port)
  loop = asyncio.get_event_loop()
  server_coro = asyncio.start_server(handle_queries, address, port, loop=loop)  # 运行结束后，返回的协程对象返回一个 asyncio.Server 实例，即一个 TCP 服务器
  server = loop.run_until_complete(server_coro)  # 驱动 server_coro 协程，启动服务器
  host = server.sockets[0].getsockname()  # 获取服务器的第一个套接字端口
  print('Serving on {}. Hit CTRL-C to stop.'.format(host))  # 在服务器的控制台显示出来
  try:
    loop.run_forever()  # 运行事件循环，main() 函数在这里阻塞，直到在服务器的控制台中按 CTRL-C 才会关闭
  except KeyboardInterrupt:
    pass

  print('Server shutting down.')
  server.close()  # 关闭服务器
  loop.run_until_complete(server.wait_closed())  # server.wait_close() 方法返回一个协程
  loop.close()


if __name__ == '__main__':
  main(*sys.argv[1:])
