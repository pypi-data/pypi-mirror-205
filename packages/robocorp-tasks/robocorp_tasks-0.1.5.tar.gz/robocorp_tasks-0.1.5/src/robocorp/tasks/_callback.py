from logging import getLogger

logger = getLogger(__name__)


class _OnExitContextManager:
    def __init__(self, on_exit):
        self.on_exit = on_exit

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.on_exit()


class Callback(object):
    """
    Note that it's thread safe to register/unregister callbacks while callbacks
    are being notified, but it's not thread-safe to register/unregister at the
    same time in multiple threads.
    """

    def __init__(self):
        self.raise_exceptions = False
        self._callbacks = ()

    def register(self, callback):
        self._callbacks = self._callbacks + (callback,)

        # Enable using as a context manager to automatically call the unregister.
        return _OnExitContextManager(lambda: self.unregister(callback))

    def unregister(self, callback):
        self._callbacks = tuple(x for x in self._callbacks if x != callback)

    def __call__(self, *args, **kwargs):
        for c in self._callbacks:
            try:
                c(*args, **kwargs)
            except:
                logger.exception(f"Error calling: {c}.")
                if self.raise_exceptions:
                    raise
