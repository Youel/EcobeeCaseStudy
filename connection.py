class Connection:
    def __init__(self, data):
        self.id = int(data[0])
        self.track_id = int(data[3])
        self.tracks = []
        self.type = "connection"

    def __str__(self):
        result = "Track " + self.id
        return result

    def get_track(self):
        return self.tracks[0]

    def get_track_ids(self):
        return [self.track_id]

    def add_track(self, track):
        self.tracks.append(track)