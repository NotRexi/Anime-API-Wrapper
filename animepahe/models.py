class Anime:
    def __init__(self, id_, title, type_, status, poster, session):
        self.id = id_
        self.title = title
        self.type = type_
        self.status = status
        self.poster = poster
        self.session = session


class Episode:
    def __init__(self, id_, anime_id, number, snapshot, audio, duration, url):
        self.id = id_
        self.anime_id = anime_id
        self.number = number
        self.snapshot = snapshot
        self.audio = audio
        self.duration = duration
        self.url = url


class Download:
    def __init__(self, url, res, fileSize, type, is_dubbed):
        self.url = url
        self.res = res
        self.fileSize = fileSize
        self.type = "Dub" if type else "Sub"
        self.downloadLink = None
        self.is_dubbed = is_dubbed
