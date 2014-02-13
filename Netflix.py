#!/usr/bin/env python3
# Paul Strong

import math
import io

BASE_CACHE_PATH = "/u/thunt/cs373-netflix-tests"

CACHE_PROBE = 0
CACHE_GENERAL = 1

cache_probe = None
cache_movie_averages = None
cache_cust_averages = None
cache_num_ratings = None
cache_movie_decade_avg = None

PROBE_MEAN = 3.7
AVG_NUM_RATINGS = 5654.5

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
    return rmse(self.predictions, self.real_ratings())

  def real_ratings(self) :
    return map(lambda x: get_cache_probe()[self.movie][x], self.custids)


def netflix_solve(r, w) :
  """
  read, eval, print loop
  r is a reader
  w is a writer
  """
  netflix_load_caches()

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
  netflix_load_caches()
  predicted_ratings = []
  for custid in custids:
    rating = cache_movie_decade_avg[movie] + (cache_movie_averages[movie] - cache_movie_decade_avg[movie]) + (cache_cust_averages[custid] - PROBE_MEAN)
    # rating = rating / 4
    rating = max(min(rating, 5.0), 1.0) # Ratings can only be between 1.0 and 5.0
    predicted_ratings.append(rating)
  prediction = Prediction(movie, custids, predicted_ratings)
  assert(prediction is not None)
  return prediction

  # with open("irvin-user_avg_json", "r")
  # 
def netflix_load_caches():
  get_cache_probe()
  global cache_movie_averages
  global cache_cust_averages
  global cache_num_ratings
  global cache_movie_decade_avg
  cache_movie_averages = cache_movie_averages or netflix_load_cache(CACHE_GENERAL, "ericweb2-movieAveragesOneLine.txt")
  cache_cust_averages = cache_cust_averages or netflix_load_cache(CACHE_GENERAL, "ericweb2-custAveragesOneLine.txt")
  cache_num_ratings = cache_num_ratings or netflix_load_cache(CACHE_GENERAL, "ericweb2-numRatingsOneLine.txt")
  cache_movie_decade_avg = cache_movie_decade_avg or netflix_load_cache(CACHE_GENERAL, "ericweb2-movieDecadeAvgRatingOneLine.txt")

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

  # Calculate RMSE
  predicted_ratings = [item for sublist in [prediction.predictions for prediction in predictions] for item in sublist] # flatten
  real_ratings = [item for sublist in [prediction.real_ratings() for prediction in predictions] for item in sublist] # flatten
  final_rmse = rmse(predicted_ratings, real_ratings)


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