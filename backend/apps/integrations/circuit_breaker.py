"""
Circuit breaker for national-system calls (docs/09): when an integration (NIDA, KWIVUZA…)
starts failing, the breaker opens so the platform degrades gracefully instead of hanging,
then half-opens after a cool-off to probe recovery. Pure + unit-tested (injectable clock).
"""
import time


class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, reset_timeout: float = 30.0, clock=time.monotonic):
        self.failure_threshold = failure_threshold
        self.reset_timeout = reset_timeout
        self._clock = clock
        self.failures = 0
        self.opened_at = None
        self.state = "closed"  # closed | open | half_open

    def allow(self) -> bool:
        """True if a call may proceed."""
        if self.state == "open":
            if self._clock() - self.opened_at >= self.reset_timeout:
                self.state = "half_open"
                return True
            return False
        return True

    def record_success(self):
        self.failures = 0
        self.opened_at = None
        self.state = "closed"

    def record_failure(self):
        self.failures += 1
        if self.state == "half_open" or self.failures >= self.failure_threshold:
            self.state = "open"
            self.opened_at = self._clock()
