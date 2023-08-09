import asyncio
import pproxy
import time

async def run_proxy():
    # pproxy -l http://:8888 -r socks5://93.188.207.49:59101#staniaskz:WiRhdJv7ty
    server = pproxy.Server('socks5://:8888')
    remote = pproxy.Connection('socks5://93.188.207.49:59101#staniaskz:WiRhdJv7ty')
    args = dict( rserver = [remote],
                verbose = print
                )
    print('Serving on', server.bind, 'by', ",".join(i.name for i in server.protos) + ('(SSL)' if server.sslclient else ''), '({}{})'.format(server.cipher.name, ' '+','.join(i.name() for i in server.cipher.plugins) if server.cipher and server.cipher.plugins else '') if server.cipher else '')
    loop = asyncio.get_event_loop()
    handler = await server.start_server(args)
    try:
        print("Loop started")
        loop.run_forever()
        print("Loop stopping...")
    except KeyboardInterrupt:
        print('exit!')
    finally:
        print("Loop closing...")
        handler.close()
        await handler.wait_closed()
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
        print("Loop closed")

async def mytask():
    print("mytask will be running 15 sec.")
    result = await asyncio.sleep(15, result=555)
    return result

async def main():
    # Create a "cancel_me" Task
    task = asyncio.create_task(mytask(), name='mytask')

    # Wait for 5 second
    await asyncio.sleep(5)

    # task.cancel()
    try:
        await task
        print(f"mytask finished successfully with result={task.result()}")
    except asyncio.CancelledError:
        print(f"main(): mytask is cancelled now with result=")

asyncio.run(main())