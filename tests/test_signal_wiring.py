"""Per-mode pytest view of tools/smoke_test.py's static signal-wiring check
- reuses its function rather than duplicating the regex logic, so this file
and `python tools/smoke_test.py` never drift apart. Gives each mode its own
test id (test_signal_wiring[2d], ...) instead of one aggregate pass/fail
list.

Deliberately does NOT wrap smoke_test.py's per-mode check_launches() dynamic
check here: it waits out a fixed 6s "still alive" timeout per mode (by
design - see its own docstring), which is ~90s across all 15 modes and
would blow well past this suite's ~3 minute budget for coverage that
test_handlers.py's import_mode() already mostly subsumes (it imports every
mode's top-level code - the same code check_launches() exercises - as part
of running its own handler tests, just without waiting out app.exec()).
Run `python tools/smoke_test.py` directly for the full per-mode dynamic
check (including the final "does the blocking run() call itself crash"
step this suite skips) - unchanged, still the right tool for that.
"""
import pytest
import smoke_test


@pytest.mark.parametrize("mode", smoke_test.MODES)
def test_signal_wiring(mode):
    failures = smoke_test.check_signal_wiring(mode)
    assert not failures, "; ".join(failures)
