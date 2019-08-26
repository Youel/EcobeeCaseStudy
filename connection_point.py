class ConnectionPoint:
    def __init__(self, data):
        self.id = int(data[0])
        self.cf_0_id = int(data[2])
        self.cf_1_id = int(data[3])

    def __str__(self):
        result = "Track " + self.id
        return result