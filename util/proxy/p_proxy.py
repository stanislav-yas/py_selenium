import asyncio
import sys

class Pproxy:
    LOCAL_PORT_NUM = 8880

    def __init__(self, scheme, host, port, user=None, pwd=None) -> None:
        self._scheme = scheme
        self._lport = Pproxy.LOCAL_PORT_NUM
        self.host = host
        self.port = port
        self._user = user
        self._pwd = pwd
        self._process = None
        
    async def _start_process(self):
        args = f'-m pproxy -l {self._scheme}://:{self._lport} -r {self._scheme}://{self.host}:{self.port}'
        if self._user is not None:
            args += f'#{self._user}'
            if self._pwd is not None:
                args += f':{self._pwd}'
        self._process = await asyncio.create_subprocess_exec(sys.executable, *args.split())
        Pproxy.LOCAL_PORT_NUM += 1 # TODO port number limitation

    @property
    def is_running(self):
        return self._process is not None

    def start(self):
        if not self.is_running:
            asyncio.run(self._start_process())

    def stop(self):
        if self._process is not None:
            self._process.terminate()
            self._process = None

    def __del__(self):
        if  self._process is not None:
            self._process.terminate()
            print(f'Process pid={self._process.pid} terminated')

    def __repr__(self) -> str:
        res = f"Pproxy [{self._scheme}://:{self._lport} => {self._scheme}://{self.host}:{self.port} - "
        if self._process is not None:
            res += f'running (PID:{self._process.pid})]'
        else:
            res += 'not running]'
        return  res
