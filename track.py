class Track:
    def __init__(self, data):
        self.id = int(data[0])
        self.length = int(data[2])
        self.cf_0_id = int(data[3])
        self.cf_1_id = int(data[4])
        self.train = None
        self.signals = [None, None]

        self.asking_for_lock = []
        self.holding_lock = None

    def __str__(self):
        #result = "Track " + str(self.id)
        result = (self.cf_0).__class__.__name__ + "="+ str(self.id) + "=" + (self.cf_1).__class__.__name__ + "|" + self.cf_1.next_to.__class__.__name__
        return result

    def get_next_track(self, direction):
        cf = None
        if direction == 0 :
            cf = self.cf_0
        else:
            cf = self.cf_1

        cf_next_to = cf.next_to
        next_track = cf_next_to.get_track()
        return next_track
        

    def has_train(self):
        if self.train is not None:
            return True
        return False

    def add_train(self, train):
        if self.has_train():
            print("Track already has train. Collision occured")
            return False
        train.track = self
        self.train = train
        return True

    def get_visual_str(self, train_str):
        track_length = self.length
        track_str = "=" * track_length
        if self.train is not None:
            train_str = self.train.get_train_symbol()
        if train_str is not None:
            half = track_length/2
            track_str = track_str[:half] + train_str + track_str[half+2:]
        if self.signals[0] is not None:
            track_str = self.signals[0].get_state_code() + track_str
        if self.signals[1] is not None:
            track_str = track_str + self.signals[1].get_state_code()
        return track_str

    def add_signal(self, signal):
        if self.signals[signal.track_side] is not None:
            print("Track " + str(self.track_id) + " already has a signal on side" + str(signal.track_side))
            return False
        self.signals[signal.track_side] = signal

    def get_signal(self, side):
        return self.signals[side]

    def lock(self, signal):
        if self.holding_lock is signal:
            #print("Lock track " + str(self.id))
            return True
        elif self.holding_lock is None and self.train is None:
            self.holding_lock = signal
            #print("Lock track " + str(self.id))
            return True
        else:
            #print("Lock busy: waiting")
            if signal not in self.asking_for_lock:
                self.asking_for_lock.append(signal)
            return False

    def unlock(self, signal):
        #print("UnLock track " + str(self.id))
        if self.holding_lock is None:
            print("Error, this was not locked to begin with")
            return False
        
        if self.holding_lock is not signal:
            print("Error, wrong signal trying to release lock")

        self.holding_lock = None

        if len(self.asking_for_lock) > 0:
            new_track_locker = self.asking_for_lock.pop(0)
            self.holding_lock = new_track_locker

