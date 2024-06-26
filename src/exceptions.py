class ArchiveAlreadyDownloaded(Exception):
    def __init__(self, archive_name):
        message = f"Archive {archive_name} is already exists"
        super(ArchiveAlreadyDownloaded, self).__init__(message)


class DateIsTooLate(Exception):
    def __init__(self, date):
        message = f"Gotten date {date} must be early then today"
        super(DateIsTooLate, self).__init__(message)


class IncorrectDate(Exception):
    def __init__(self, date):
        message = f"Incorrect date format, should be YYYY-MM-DD, not '{date}'"
        super(IncorrectDate, self).__init__(message)

class NoDataInStorage(Exception):
    def __init__(self, date):
        message = f"No data for date {date} in storage"
        super(NoDataInStorage, self).__init__(message)
