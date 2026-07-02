from apps.integrations.circuit_breaker import CircuitBreaker


class FakeClock:
    def __init__(self):
        self.t = 0.0

    def __call__(self):
        return self.t


def test_opens_after_threshold():
    cb = CircuitBreaker(failure_threshold=3, clock=FakeClock())
    for _ in range(3):
        cb.record_failure()
    assert cb.state == "open"
    assert cb.allow() is False


def test_half_open_after_timeout_then_close_on_success():
    clock = FakeClock()
    cb = CircuitBreaker(failure_threshold=1, reset_timeout=30, clock=clock)
    cb.record_failure()
    assert cb.allow() is False          # still open
    clock.t = 31
    assert cb.allow() is True           # half-open probe allowed
    assert cb.state == "half_open"
    cb.record_success()
    assert cb.state == "closed"


def test_half_open_failure_reopens():
    clock = FakeClock()
    cb = CircuitBreaker(failure_threshold=1, reset_timeout=10, clock=clock)
    cb.record_failure()
    clock.t = 11
    cb.allow()                          # -> half_open
    cb.record_failure()                 # fails again
    assert cb.state == "open"


def test_success_resets_failure_count():
    cb = CircuitBreaker(failure_threshold=3, clock=FakeClock())
    cb.record_failure()
    cb.record_success()
    cb.record_failure()
    assert cb.state == "closed"
