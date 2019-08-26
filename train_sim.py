import sys
import json

from train import Train
from track import Track
from connection_function import ConnectionFunction
from connection_point import ConnectionPoint
from tsignal import TSignal

from connection import Connection
from junction import Junction
from terminator import Terminator

trains_map = {}
tracks_map = {}
connection_points_map = {}
connection_functions_map = {}
signals_map = {}

obj_maps = {
            "train" : trains_map,
            "track" : tracks_map,
            "connection_point" : connection_points_map,
            "connection_function" : connection_functions_map,  
            "signal": signals_map
           }

def create_train(data):
  train = Train(data)
  return train

def create_track(data):
  track = Track(data)
  return track

def create_connection_point(data):
  connection_point = ConnectionPoint(data)
  return connection_point

def create_connection_function(data):
  connection_function = None
  con_type = data[2]
  if con_type == "terminator":
    connection_function = Terminator(data)
  elif con_type == "junction":
    connection_function = Junction(data)
  elif con_type == "connection":
    connection_function = Connection(data)
  return connection_function

def create_signal(data):
  signal = TSignal(data)
  return signal

def create_object(data):
  print("Create Object for Data: " + str(data))
  obj_id = int(data[0])
  obj_type = data[1]
  obj_map = None
  obj = None

  if obj_type == "train":
    obj = create_train(data)
  elif obj_type == "track":
    obj = create_track(data)
  elif obj_type == "connection_point":
    obj = create_connection_point(data)
  elif obj_type == "connection_function":
    obj = create_connection_function(data)
  elif obj_type == "signal":
    obj = create_signal(data)
  else:
    return "Couldn't find type " + obj_type
  
  if obj_type not in obj_maps:
    return "No map for " + obj_type + " exists"
  else:
    obj_map = obj_maps[obj_type]
  if (obj_id) in obj_map:
    return obj_type + " table has conflicting id's> id: " + str(obj_id)
  obj_map[(obj_id)] = obj

  return None

def link_sim_objects():
  print("link_sim_objects")
  for cp_id in connection_points_map:
    print(cp_id)
    cp = connection_points_map[cp_id]
    cf0 = connection_functions_map[cp.cf_0_id]
    cp.cf_0 = cf0
    cf1 = connection_functions_map[cp.cf_1_id]
    cp.cf_1 = cf1
    cf0.next_to = cf1
    cf1.next_to = cf0

  for cf_id in connection_functions_map:
    cf = connection_functions_map[cf_id]
    track_ids = cf.get_track_ids()
    print("CF " + str(cf.id) + " has these tracks connected to it: " + str(track_ids))
    for i in range(0, len(track_ids)):
      track_id = track_ids[i]
      if track_id not in tracks_map:
        print("Track Id " + str(track_id) + " DNE; Check Config")
        return False
      track = tracks_map[track_id]
      cf.add_track(track)

  for train_id in trains_map:
    train = trains_map[train_id]
    track = tracks_map[train.start_track_id]
    if track.has_train():
      return "Track " + train.start_track_id + " has a train on it already"
    train.track = track
    track.train = train

  for track_id in tracks_map:
    track = tracks_map[track_id]
    cf = connection_functions_map[track.cf_0_id]
    track.cf_0 = cf
    cf = connection_functions_map[track.cf_1_id]
    track.cf_1 = cf
    
  for signal_id in signals_map:
    signal = signals_map[signal_id]
    track = tracks_map[signal.track_id]
    track.add_signal(signal)
    for lock_track_ids in signal.lock_track_ids:
      lock_track = tracks_map[lock_track_ids]
      signal.add_track_locks(lock_track)

def create_sim_objects(file):
  for line in file:
    data_split = line.split(",")
    result = create_object(data_split)
    if result is not None:
      print(result)
      return False      

  print("Signals_map " + str(signals_map))
  return link_sim_objects()

def print_train_perspecive(train):
    print("Train-" + str(train.id) + ": " + train.get_visual_str())


def display_end_result():
  print("End Result")

  for train_id in trains_map:
    train = trains_map[train_id]
    print_train_perspecive(train)

def run_simulation():
  print("run_simulation")
  turns = 0
  consecutive_stops = 0
  while(turns < 15):
    print("Update " + str(turns))
    stopped_trains = set()
    moving_trains = set()
    for train_id in trains_map:
      train = trains_map[train_id]
      print_train_perspecive(train)

      if train.update() is False:
        print("An Error has occured. Sim Failed")
        return False
      if train.is_stopped():
        stopped_trains.add(train)
      else:
        moving_trains.add(train)
    if consecutive_stops > 2:
      print("Ending Sim; All Trains Stopped")
      break
    elif len(moving_trains) == 0:
      consecutive_stops += 1
    else:
      consecutive_stops = 0
    turns += 1
  
  display_end_result()

def load_file(file_name):
	data_file_name = file_name
  	data_file = open(data_file_name, "r")
  	return data_file

def main():
  print(str(sys.argv))
  file_name=  sys.argv[1]
  file = load_file(file_name)
  if create_sim_objects(file) is False:
    print("Failed to Create Sim Objects")
    return -1

  run_simulation()

if __name__== "__main__":
  main()