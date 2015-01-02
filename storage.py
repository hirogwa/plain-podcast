from django.core.files.storage import FileSystemStorage
import plainpodcast.settings as settings


class PrivateStorage(FileSystemStorage):
    def __init__(self, location=None, base_url=None):
        if location is None:
            location = settings.PRIVATE_FILE_ROOT
        if base_url is None:
            base_url = settings.PRIVATE_FILE_URL
        return super(PrivateStorage, self).__init__(location, base_url)

    def save(self, name, content):
        if self.exists(name):
            self.delete(name)
        return super(PrivateStorage, self).save(name, content)
