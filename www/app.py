# -*- coding: utf-8 -*-

import asyncio
from aiohttp import web

async def index(request):
    return web.Response(body=b'<a>hello</a>', content_type='text/html')


async def init(loop):
    app = web.Application(loop=loop)
    app.router.add_route("GET", '/', index)
    server = await loop.create_server(app.make_handler(), '0.0.0.0', 8956)
    print("server started at 8956")
    return server


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init(loop))
    loop.run_forever()


if __name__ == '__main__':
    main()
