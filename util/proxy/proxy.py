import asyncio
import sys

class Proxy:
    LOCAL_PORT_NUM = 8880

    def __init__(self, scheme, host, port, user=None, pwd=None) -> None:
        self._scheme = scheme
        self._host = host
        self._port = port
        self._user = user
        self._pwd = pwd
        self._started = False
        self._process = None
        
    async def _start_process(self):
        lport = Proxy.LOCAL_PORT_NUM
        args = f'-m pproxy -l {self._scheme}://:{lport} -r {self._scheme}://{self._host}:{self._port}'
        if self._user is not None:
            args += f'#{self._user}'
            if self._pwd is not None:
                args += f':{self._pwd}'
        self._process = await asyncio.create_subprocess_exec(sys.executable, *args.split())
        self._started = True
        Proxy.LOCAL_PORT_NUM += 1 # TODO port number limitation

    @property
    def started(self):
        return self._started

    def start(self):
        if not self._started:
            asyncio.run(self._start_process())

    def stop(self):
        if self._started and self._process is not None:
            self._process.terminate()
            self._process = None
            self._started = False

    def __del__(self):
        if  self._started and self._process is not None:
            self._process.terminate()
            print(f'Process pid={self._process.pid} terminated')
