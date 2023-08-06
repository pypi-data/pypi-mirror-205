class DQLError(RuntimeError):
    pass


class NotFoundError(Exception):
    pass


class DatasetNotFoundError(NotFoundError):
    pass


class StorageNotFoundError(NotFoundError):
    pass
