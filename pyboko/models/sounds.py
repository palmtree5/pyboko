class SoundsData:
    def __init__(self, data):
        self.updated = data.get("updated", None)
        self.matching = data.get("matching", None)
        self.sounds = [Sound(sound) for sound in data.get("sounds", [])]


class Sound:
    def __init__(self, data):
        self.amount = data.get("amount", None)
        self.description = data.get("description", None)
        self.verified = data.get("verified", None)
        self.newsound = data.get("newsound", None)
        self.matched = data.get("matched", None)