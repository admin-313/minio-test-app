class ImageDatabaseException(Exception):
    pass

class EmptyBucketException(ImageDatabaseException):
    pass

class BucketDoesNotExistException(ImageDatabaseException):
    pass