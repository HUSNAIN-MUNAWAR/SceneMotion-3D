from threading import Thread
from typing import Callable

class LocalTaskRunner:
    def submit(self, fn: Callable, *args, **kwargs) -> Thread:
        t = Thread(target=fn, args=args, kwargs=kwargs, daemon=True)
        t.start()
        return t
