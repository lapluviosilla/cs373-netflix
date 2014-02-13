#!/usr/bin/env python3
# Paul Strong

import math
import io

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

def rmse(a, b) :
  """
  Calculate Root Mean Squared Error between two iterables a and b
  """
  z = zip(a, b)
  v = sum(((x - y) ** 2 for x, y in z), 0.0)
  return math.sqrt(v / len(a))