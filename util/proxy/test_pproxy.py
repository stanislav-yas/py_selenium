import asyncio
import sys
import time
import pproxy
from proxy import Proxy

async def run_proxy():
    # pproxy -l socks5://:8888 -r socks5://93.188.207.49:59101#staniaskz:WiRhdJv7ty
    server = pproxy.Server('socks5://:8888')
    remote = pproxy.Connection('socks5://93.188.207.49:59101#staniaskz:WiRhdJv7ty')
    args = dict( rserver = [remote],
                verbose = print
                )
    print('Serving on', server.bind, 'by', ",".join(i.name for i in server.protos) + ('(SSL)' if server.sslclient else ''), '({}{})'.format(server.cipher.name, ' '+','.join(i.name() for i in server.cipher.plugins) if server.cipher and server.cipher.plugins else '') if server.cipher else '')
    loop = asyncio.get_event_loop()
    handler = loop.run_until_complete(server.start_server(args))
    try:
        print("Loop started")
        loop.run_forever()
        print("Loop stopping...")
    except KeyboardInterrupt:
        print('exit!')
    finally:
        print("Loop closing...")
        handler.close()
        loop.run_until_complete(handler.wait_closed())
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
        print("Loop closed")

async def start_proxy():
    args = "-m ppproxy -l socks5://:8888 -r socks5://212.8.229.77:59101#staniaskz:WiRhdJv7ty".split()
    # sys.executable, '-m pproxy'
    proc = await asyncio.create_subprocess_exec(sys.executable, *args)
    # await proc.wait()
    return proc

proxy = Proxy('socks5', '212.8.229.77', '59101', 'staniaskz', 'WiRhdJv7ty')
if not proxy.started:
    proxy.start()
time.sleep(5)
# proxy.stop()
# proc = asyncio.run(start_proxy())
# print(proc.pid)
# proc.terminate()
proxy = None
pass