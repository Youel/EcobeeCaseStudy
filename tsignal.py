class TSignal:
    def __init__(self, data):
        self.id = int(data[0])
        self.track_id = int(data[2])
        self.track_side =int(data[3])
        self.lock_track_ids = []
        self.lock_tracks = []
        self.locked_tracks = []
        split_ids = data[4].split(':')
        for item in split_ids:
            self.lock_track_ids.append(int(item))
        self.state = "R"

    def __str__(self):
        result = "Track " + self.id
        return result

    def get_state_code(self):
        return self.state

    def get_green(self):
        result = True
        for track in self.lock_tracks:
            if track in self.locked_tracks:
                continue
            result = track.lock(self)
            if result:
                self.locked_tracks.append(track)
        
        if result:
            self.state = "G"

        return result
    
    def add_track_locks(self, track):
        self.lock_tracks.append(track)

    def train_moved(self, new_track):
        if new_track not in self.lock_tracks:
            print("No longer need the signal to be green")
        else:
            return False

        for track in self.locked_tracks:
            track.unlock(self)
        
        self.locked_tracks =[]

        self.state = "R"

        return True
        