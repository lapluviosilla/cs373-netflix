#!/usr/bin/env python3
# Paul Strong

import math
import io

BASE_CACHE_PATH = "../netflix-tests/"

CACHE_PROBE = 0
CACHE_GENERAL = 1

cache_probe = {}

class Prediction:
  def __init__(self, movie, custids, predictions):
    self.movie = movie
    self.custids = custids
    self.predictions = predictions

  def display(self, writer):
    writer.write(str(self.movie) + ":\n")
    for rating in self.predictions:
      writer.write(str(round(rating, 1)) + "\n") 

  def calculate_rmse(self) :
    return rmse(self.predictions, map(lambda x: get_cache_probe()[self.movie][x], self.custids))


def netflix_solve(r, w) :
  """
  read, eval, print loop
  r is a reader
  w is a writer
  """
  get_cache_probe() # Load probe cache if it has not been loaded yet

  assert(len(cache_probe) > 0)

  predictions = []

  movie = 0
  custids = []
  for line in r:
    if line.strip().endswith(":"):
      if len(custids) > 0:
        # at end of movie
        predictions.append(netflix_predict(movie, custids))
        custids = []
      line = line.strip().rstrip(":")
      movie = int(line)
      # w.write(line + ":\n")
    else:
      custid = int(line)
      custids.append(custid)
      # w.write(str(3.7) + "\n")
  if len(custids) > 0 : predictions.append(netflix_predict(movie, custids))

  assert(len(predictions) > 0)
  netflix_print(w, predictions)

def netflix_predict(movie, custids) :
  assert(movie > 0)
  assert(len(custids) > 0)
  prediction = Prediction(movie, custids, len(custids) * [3.7])
  assert(prediction is not None)
  return prediction

  # with open("irvin-user_avg_json", "r")

def netflix_load_cache(cache_type, path):
  """
  reads and loads different caches into dictionary
  cache_type can be either CACHE_PROBE or CACHE_GENERAL depending
  on whether you want to load a probe cache or a general cache
  """
  cache = {}
  
  with open(BASE_CACHE_PATH + path, "r") as f:
    if cache_type == CACHE_PROBE:
      current_id = 0
      for line in f:
        # If the line ends with a : then it is indicating the movie id
        if line.strip().endswith(":"):
          current_id = int(line.strip().rstrip(":"))
          cache[current_id] = {}
        else:
          # This line is a customer and a rating
          custid, rating = (line.strip().split("-"))
          cache[current_id][int(custid)] = int(rating)
    elif cache_type == CACHE_GENERAL:
      # split each line by colon and create a generator
      split_g = (line.strip().split(": ") for line in f)
      # use a dictionary comprehension to build our cache from the split values
      cache = { int(key): float(val) for key, val in split_g }

  return cache

def netflix_print(w, predictions) :
  for prediction in predictions :
    prediction.display(w)

  v = sum((prediction.calculate_rmse() ** 2 for prediction in predictions), 0.0)
  final_rmse = math.sqrt(v / len(predictions))

  w.write("RMSE: " + str(final_rmse) + "\n")

def rmse(a, b) :
  """
  Calculate Root Mean Squared Error between two iterables a and b
  """
  z = zip(a, b)
  v = sum(((float(x) - float(y)) ** 2 for x, y in z), 0.0)
  return math.sqrt(v / len(a))

def get_cache_probe():
  global cache_probe
  cache_probe = cache_probe or netflix_load_cache(CACHE_PROBE, "word-probeMapCache.txt")
  return cache_probe
def set_cache_probe(val):
  global cache_probe
  cache_probe = val