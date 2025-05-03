# -*- coding: utf-8 -*-
# Author: Timur Gilmullin


import pytest
import time
import threading
from tksbrokerapi.TKSBrokerAPI import RateLimiter


TKS_METHOD_LIMITS = {
    "testMethod": 3,
    "default": 2
}


class TestRateLimiter:

    @pytest.fixture(scope="function")
    def limiter(self):
        rl = RateLimiter(methodLimits=TKS_METHOD_LIMITS)
        rl.moreDebug = False

        return rl

    def test_CheckRateLimitCheckType(self, limiter):
        limiter.CheckRateLimit("testMethod")

        assert isinstance(limiter.counters["testMethod"], int)
        assert isinstance(limiter.timestamps["testMethod"], float)

    def test_CheckRateLimitPositive(self, limiter):
        for _ in range(3):
            limiter.CheckRateLimit("testMethod")

        assert limiter.counters["testMethod"] == 3

    def test_CheckRateLimitBlockThenReset(self, limiter):
        """
        Verifies that CheckRateLimit enforces blocking after the limit is exceeded —
        without waiting for a real 60-second interval.
        """
        # Call the method to reach the rate limit:
        for _ in range(3):
            limiter.CheckRateLimit("testMethod")

        # Emulate that nearly 60 seconds have passed since the window started:
        limiter.timestamps["testMethod"] -= 59.5

        t0 = time.monotonic()
        limiter.CheckRateLimit("testMethod")  # Should not block due to nearly expired window
        elapsed = time.monotonic() - t0

        assert elapsed < 1.0  # Should proceed immediately
        assert limiter.counters["testMethod"] >= 1

    def test_HandleServerRateLimitBlocksAndResets(self, limiter):
        """
        Verifies that HandleServerRateLimit resets counters correctly —
        without actually sleeping for the full duration.
        """
        # Simulate server-enforced wait, but skip real delay by patching `sleep`:
        originalSleep = time.sleep

        try:
            time.sleep = lambda s: None  # override sleep with no-op

            limiter.HandleServerRateLimit("testMethod", 2)

            assert limiter.counters["testMethod"] == 0
            assert abs(time.monotonic() - limiter.timestamps["testMethod"]) < 1.0

        finally:
            time.sleep = originalSleep  # restore original sleep

    def test_ParallelEventSync(self, limiter):
        def call():
            limiter.CheckRateLimit("testMethod")

        threads = [threading.Thread(target=call) for _ in range(3)]

        for t in threads: t.start()
        for t in threads: t.join()

        assert limiter.counters["testMethod"] == 3

    def test_MultipleMethodsIsolated(self, limiter):
        """
        Verifies that separate method counters are isolated and do not interfere with each other.
        """
        for _ in range(2):
            limiter.CheckRateLimit("testMethod")     # Uses limit = 3
            limiter.CheckRateLimit("anotherMethod")  # Uses default limit = 2

        assert limiter.counters["testMethod"] == 2
        assert limiter.counters["anotherMethod"] == 2

        # Reaching limit on 'anotherMethod' should not block 'testMethod'
        limiter.CheckRateLimit("testMethod")
        assert limiter.counters["testMethod"] == 3

    def test_ManualMethodNameOverride(self, limiter):
        """
        Verifies that manually specified methodName is honored and used for rate limiting.
        """
        limiter.methodLimits["CustomMethod"] = 5  # Set a high enough limit to avoid blocking

        for _ in range(3):
            limiter.CheckRateLimit("CustomMethod")

        assert limiter.counters["CustomMethod"] == 3
