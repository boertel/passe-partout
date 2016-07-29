class Locking(object):
    LOCK_PATH = '.lock'
    UNLOCK_MESSAGE = 'unlock'
    LOCK_MESSAGE = 'lock'
    LOCK_CONTENT = ''

    def __init__(self, owner, repo, log=None):
        self.owner = owner
        self.repo = repo
        self.log = log or self._empty

    def lock(self):
        raise NotImplementedError()

    def unlock(self):
        raise NotImplementedError()

    def is_locked(self):
        raise NotImplementedError()

    def _empty(self, *args, **kwargs):
        # empty on purpose
        pass

    def _log(self, *args, **kwargs):
        self.log(*args, **kwargs)
