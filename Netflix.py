#!/usr/bin/env python3
# Paul Strong

import math



def rmse(a, b) :
  """
  Calculate Root Mean Squared Error between two iterables a and b
  """
  z = zip(a, b)
  v = sum(((x - y) ** 2 for x, y in z), 0.0)
  return math.sqrt(v / len(a))