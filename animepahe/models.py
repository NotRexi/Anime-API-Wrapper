class Anime:
    def __init__(self, id_, title, type_, status, poster, session):
        self.id = id_
        self.title = title
        self.type = type_
        self.status = status
        self.poster = poster
        self.session = session


class Episode:
    def __init__(self, id_, anime_id, number, snapshot, duration, url):
        self.id = id_
        self.anime_id = anime_id
        self.number = number
        self.snapshot = snapshot
        self.duration = duration
        self.url = url


class Download:
    def __init__(self, url, res, fileSize, is_dubbed):
        self.url = url
        self.res = res
        self.fileSize = fileSize
        self.downloadLink = None
        self.is_dubbed = is_dubbed

    @property
    def label(self):
        """Dynamic display label based on is_dubbed."""
        return "Dub" if self.is_dubbed else "Sub"
