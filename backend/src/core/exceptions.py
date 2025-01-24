class MissingSettings(Exception):
    pass


class InvalidInputError(Exception):
    pass


class DatabaseError(Exception):
    pass


class ImageProcessError(Exception):
    pass


class NoResultsFound(Exception):
    pass


class CustomErrorMessage(Exception):
    pass


class CacheError(Exception):
    pass
