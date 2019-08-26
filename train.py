class Train:
    def __init__(self, data):
        self.id = int(data[0])
        self.direction = int(data[2])
        self.start_track_id = int(data[3])
        self.state = "stopped"
        self.at_terminator = False
        self.signal_holding = None

    def __str__(self):
        result = "Train " + str(self.id) + " on track " + str(self.track.id) +  " going " + str(self.direction)
        return result

    def get_train_symbol(self):
        
        result = ""
        if self.state == "stopped":
            result += "s"
        else:
            result +="g"

        if self.direction == 0 :
            result = "<" + result
        else:
            result = result + ">"
        return result

    def get_visual_str(self):
        #print("Printing Train")
        result = self.get_train_symbol()

        result = self.track.get_visual_str(result)
        next_track = self.track
        print_tracks = set()
        while (True):
            #print(str(print_tracks))
            print_tracks.add(next_track)
            next_track = next_track.get_next_track(1)
            if next_track in print_tracks:
                break
            if next_track == "Terminator":
                result += "|" + "E"
                break
            else:
                result += "|" + next_track.get_visual_str(None)

        next_track = self.track
        #print(str(print_tracks))
        while (True):
            print_tracks.add(next_track)
            next_track = next_track.get_next_track(0)
            if next_track in print_tracks:
                break
            if next_track == "Terminator":
                result = "E"  + "|" + result
                break
            else:
                result = next_track.get_visual_str(None)  + "|" + result 

        #print("Done")
        return result

    def switch_tracks(self, next_track):
        current_track = self.track
        current_track.train = None
        result = next_track.add_train(self) 
        if result:
            if self.signal_holding is not None:
                if self.signal_holding.train_moved(next_track):
                    self.signal_holding= None
            i = 0
            #print("Train Switched from Track " + str(current_track.id) + " to Track " + str(self.track.id))

        return result

    def update(self):
        result = True
        if self.at_terminator is True:
            return result
        
        signal = self.track.get_signal(self.direction)
        next_track = self.track.get_next_track(self.direction)

        if signal is not None:
            should_stop = signal.state == "R"
            got_green = signal.get_green()
            if should_stop:
                self.state = "stopped"
                return True
            elif got_green == True:
                print("Got the Green")
                self.state = "going"
                i = 0
                self.signal_holding = signal
            else:
                self.state = "stopped"
                return
        if next_track == "Terminator":
            self.state = "stopped"
            self.at_terminator = True
            print("Train is at a Terminator")
        else:
            if self.state == "stopped":
                self.state="going"
            else:
                result = self.switch_tracks(next_track)

        return result

    def is_stopped(self):
        if self.state == "stopped":
            return True
        return False