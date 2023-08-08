import asyncio
import pproxy

# pproxy -l http://:8888 -r socks5://93.188.207.49:59101#staniaskz:WiRhdJv7ty
server = pproxy.Server('http://:8888')
remote = pproxy.Connection('socks5://93.188.207.49:59101#staniaskz:WiRhdJv7ty')
args = dict( rserver = [remote],
             verbose = print
            )

loop = asyncio.get_event_loop()
handler = loop.run_until_complete(server.start_server(args))
try:
    loop.run_forever()
except KeyboardInterrupt:
    print('exit!')

handler.close()
loop.run_until_complete(handler.wait_closed())
loop.run_until_complete(loop.shutdown_asyncgens())
loop.close()