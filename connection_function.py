class ConnectionFunction:
    def __init__(self, data):
        self.id = int(data[0])

    def __str__(self):
        result = "Track " + self.id
        return result