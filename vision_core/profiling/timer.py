from __future__ import annotations
import time
from contextlib import contextmanager

class StageTimer:
    def __init__(self):
        self.timings = {}

    @contextmanager
    def stage(self, name: str):
        start = time.perf_counter()
        try:
            yield
        finally:
            self.timings[name] = self.timings.get(name, 0.0) + (time.perf_counter() - start)

    def summary(self):
        return {k: round(v, 6) for k, v in self.timings.items()}
