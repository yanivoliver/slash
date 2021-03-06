from __future__ import print_function

import threading
from contextlib import contextmanager

try:
    from IPython import embed # pylint: disable=F0401
except ImportError:
    import code
    def _interact(ns):
        code.interact(local=ns)
else:
    def _interact(ns):
        embed(user_ns=ns)

def start_interactive_shell(**namespace):
    """
    Starts an interactive shell. Uses IPython if available, else fall back
    to the native Python interpreter.

    Any keyword argument specified will be available in the shell ``globals``.
    """
    _interact(namespace)


@contextmanager
def notify_if_slow_context(message, slow_seconds=1):
    evt = threading.Event()
    def notifier():
        if not evt.wait(timeout=slow_seconds):
            print(message)
    thread = threading.Thread(target=notifier)
    thread.start()
    try:
        yield
    finally:
        evt.set()
        thread.join()
