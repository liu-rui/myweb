import logging
import asyncio

from aiohttp import web

logging.basicConfig(level=logging.INFO)
_PORT = 5689

async def index(request):
    return web.Response(body=b'Index Page', content_type='text/html')


async def init(loop):
    app = web.Application(loop=loop)
    app.router.add_route("GET", "/", index)
    server = await loop.create_server(app.make_handler(), "0.0.0.0", _PORT)
    logging.info('server started at http://localhost:%d', _PORT)
    return server


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init(loop))
    loop.run_forever()
    loop.close()


if __name__ == "__main__":
    main()
