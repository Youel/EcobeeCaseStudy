class Junction:
    def __init__(self, data):
        self.id = int(data[0])
        self.selected_line = int(data[3])
        self.track_ids = []
        self.tracks = []
        split_ids = data[4].split(':')
        for item in split_ids:
            self.track_ids.append(int(item))


    def __str__(self):
        result = "Track " + self.id
        return result

    def get_track_ids(self):
        return self.track_ids

    def get_track(self):
        return self.tracks[self.selected_line]

    def add_track(self, track):
        self.tracks.append(track)