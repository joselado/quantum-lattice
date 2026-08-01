"""The shell (bin/versions/quantum-lattice-pyqt) builds its initially-shown
page and reaches the event loop without crashing. See tools/smoke_test.py's
check_shell() for what "healthy" means here (still blocked in app.exec()
after a timeout, not a clean exit)."""
import smoke_test


def test_shell_launches():
    failures = smoke_test.check_shell()
    assert not failures, "; ".join(failures)
