from collections import deque
from time import perf_counter
from threading import Lock
from statistics import mean

class _Series:
    __slots__ = ("window", "lock", "maxlen")
    def __init__(self, maxlen=5000):
        self.window = deque(maxlen=maxlen)
        self.lock = Lock()
        self.maxlen = maxlen

    def add(self, value):
        with self.lock:
            self.window.append(float(value))

    def snapshot(self):
        with self.lock:
            data = list(self.window)
        if not data:
            return dict(count=0, avg=0.0, p50=0.0, p95=0.0, p99=0.0, min=0.0, max=0.0)
        data_sorted = sorted(data)
        n = len(data_sorted)
        def pct(p):
            if n == 1: return data_sorted[0]
            idx = min(n-1, max(0, int(round((p/100.0) * (n-1)))))
            return data_sorted[idx]
        return dict(
            count=n,
            avg=mean(data_sorted),
            p50=pct(50),
            p95=pct(95),
            p99=pct(99),
            min=data_sorted[0],
            max=data_sorted[-1],
        )

class MetricsRegistry:
    def __init__(self):
        self._series = {}
        self._lock = Lock()

    def timer(self, name):
        reg = self
        class _T:
            def __enter__(self_nonlocal):
                self_nonlocal.t0 = perf_counter()
                return self_nonlocal
            def __exit__(self_nonlocal, exc_type, exc, tb):
                dt_ms = (perf_counter() - self_nonlocal.t0) * 1000.0
                reg.add(name, dt_ms)
        return _T()

    def add(self, name, value):
        with self._lock:
            s = self._series.get(name)
            if s is None:
                s = self._series[name] = _Series()
        s.add(value)

    def snapshot(self):
        with self._lock:
            items = list(self._series.items())
        return {name: series.snapshot() for name, series in items}

# Global singleton
metrics = MetricsRegistry()
