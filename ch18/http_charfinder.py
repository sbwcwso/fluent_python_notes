import sys
import asyncio
from aiohttp import web

from charfinder import UnicodeNameIndex

TEMPLATE_NAME = 'ch18/http_charfinder.html'
CONTENT_TYPE = 'text/html;'
SAMPLE_WORDS = ('bismillah chess cat circled Malayalam digit'
                ' Roman face Ethiopic black mark symbol dot'
                ' operator Braille hexagram').split()

ROW_TPL = '<tr><td>{descr.code_str}</td><th>{descr.char}</th><td>{descr.name}</td></tr>'
LINK_TPL = '<a href="/?query={0}" title="find &quot;{0}&quot;">{0}</a>'
LINKS_HTML = ', '.join(LINK_TPL.format(word) for word in
                       sorted(SAMPLE_WORDS, key=str.upper))


index = UnicodeNameIndex()
with open(TEMPLATE_NAME) as tpl:
    template = tpl.read()
template = template.replace('{links}', LINKS_HTML)  # 渲染模板中开头的链接


def home(request):  # 路由处理函数，参数是一个 aiohttp.web.Request 实例
  query = request.query.get('query', '').strip()  # 获取查询字符，去掉首尾空白
  if query:  # 如果有查询字符串,从索引(index)中找到结果,使用 HTML 表格中的行渲染结果,把结果赋值给 res 变量,再把状态消息赋值给 msg 变量
    descriptions = list(index.find_descriptions(query))
    res = '\n'.join(ROW_TPL.format(descr = descr)
                    for descr in descriptions)
    msg = index.status(query, len(descriptions))
  else:
    descriptions = []
    res = ''
    msg = 'Enter words describing characters.'

  html = template.format(query=query, result=res, message=msg)  # 渲染 HTML 页面
  print('Sending {} results'.format(len(descriptions)))  # 在服务器的控制台中记录响应
  return web.Response(content_type=CONTENT_TYPE, text=html, charset='utf8')  # 构建 response 对象，将其返回


async def init(loop, address, port):  # init 协程产出一个服务器，交给事件循环驱动
  app = web.Application(loop=loop)  # aiohttp.web.Application 类表示 WEB 应用
  app.router.add_route('GET', '/', home)  # 通过路由把 URL 模式映射到处理函数上，如果 home 是普通的函数，则在内部会将其转换为协程
  handler = app.make_handler()  # 返回一个 aiohttp.web.RequestHandler  实例，根据 app 对象设置路由处理 HTPP 请求
  server = await loop.create_server(handler, address, port)  # create_server 方法创建服务器，以 handler 为协议处理程序，并把服务器绑定在指定的地址(address)和端口(port)上
  return server.sockets[0].getsockname(), server  # 返回第一个服务器套接字的地址和端口和 server


def main(address='127.0.0.1', port=7878):
  port = int(port)
  loop = asyncio.get_event_loop()
  host, server= loop.run_until_complete(init(loop, address, port))  # 运行 init 函数，启动服务器，获取服务器的地址和端口; 只有驱动协程，协程才能做事
  print('Serving on {}. Hit CTRL-C to stop.'.format(host))
  try:
    loop.run_forever()  # 运行事件循环，main 函数会在此处阻塞
  except KeyboardInterrupt:  # 按 CTRL-C 键
    print('Server shutting down.')
  loop.run_until_complete(server.wait_closed())  # 关闭服务器
  print('Server shutting down.')
  loop.close()  # 关闭事件循环


if __name__ == '__main__':
  main(*sys.argv[1:])
