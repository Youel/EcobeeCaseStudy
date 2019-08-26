class Terminator:
    def __init__(self, data):
        self.id = int(data[0])

    def __str__(self):
        result = "Terminator " + self.id
        return result

    def get_track(self):
        return "Terminator"
    
    def get_track_ids(self):
        return []