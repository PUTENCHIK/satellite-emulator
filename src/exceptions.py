class ArchiveAlreadyDownloaded(Exception):
    def __init__(self, archive_name):
        message = f"Archive {archive_name} is already exists"
        super(ArchiveAlreadyDownloaded, self).__init__(message)

