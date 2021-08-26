import asyncio
import re
import argparse
import ssl
import logging
import uvloop
from aiohttp import web,ClientSession

parser = argparse.ArgumentParser()
parser.add_argument('-port','--port',help='port to bind and listen on', default=80,type=int)
parser.add_argument('-rhost','--rhost',help='remote host to connect to')

args = parser.parse_args()

async def proxy_http(request):
    url = '{}{}'.format(args.rhost,request.path_qs)
    #del request.headers['Upgrade-Insecure-Requests']
    #del request.headers['DNT']
    headers = {}
    for k,v in request.headers.items():
        if k not in ('Upgrade-Insecure-Requests','DNT'):
            headers[k] = v
    print(request.method,url)
    resp = await app['client'].request(request.method,url,headers=headers)
    text = await resp.text()
    print(text)
    return web.Response(text=text,headers=resp.headers)

async def init_app(loop):
    app = web.Application()
    app.router.add_route('*', '/{tail:.*}', proxy_http)
    app['client'] = ClientSession()
    return app

loop = uvloop.new_event_loop()
asyncio.set_event_loop(loop)

if __name__ == "__main__":
    app = loop.run_until_complete(init_app(loop))
    web.run_app(
        app,
        port=args.port,
        access_log_format='%a %t "%r" %s %b "%{Referrer}i" "%{User-Agent}i" %D')
