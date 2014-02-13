#!/usr/bin/env python3
# Paul Strong

import math
import io

BASE_CACHE_PATH = "../netflix-tests/"

CACHE_PROBE = 0
CACHE_GENERAL = 1

def netflix_solve(r, w) :
  """
  read, eval, print loop
  r is a reader
  w is a writer
  """
  movie = 0
  for line in r:
    if line.strip().endswith(":"):
      line = line.strip().rstrip(":")
      movie = int(line)
      w.write(line + ":\n")
    else:
      custid = int(line)
      w.write(str(3.7) + "\n")


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



def rmse(a, b) :
  """
  Calculate Root Mean Squared Error between two iterables a and b
  """
  z = zip(a, b)
  v = sum(((x - y) ** 2 for x, y in z), 0.0)
  return math.sqrt(v / len(a))