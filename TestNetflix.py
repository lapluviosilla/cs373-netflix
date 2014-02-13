#!/usr/bin/env python3

"""
To test the program:
    % python TestNetflix.py > TestNetflix.out
    % chmod ugo+x TestNetflix.py
    % TestNetflix.py > TestNetflix.out
"""

import io
import unittest

from Netflix import netflix_solve, netflix_predict, rmse, netflix_load_cache, set_cache_probe, get_cache_probe, Prediction, CACHE_PROBE, CACHE_GENERAL

class TestNetflix (unittest.TestCase) :
  # ---
  # netflix_solve
  # ---
  def test_solve1 (self) :
    r = io.StringIO("1:\n14756\n")
    w = io.StringIO()
    netflix_solve(r, w)
    self.assertEqual(w.getvalue(), "1:\n3.7\nRMSE: 0.2999999999999998\n")

  def test_solve2 (self) :
    r = io.StringIO("1:\n712610\n1772839\n1059319\n2380848\n548064\n")
    w = io.StringIO()
    netflix_solve(r, w)
    self.assertEqual(w.getvalue(), "1:\n3.7\n3.7\n3.7\n3.7\n3.7\nRMSE: 1.0630145812734648\n")

  def test_solve3 (self) :
    r = io.StringIO("10007:\n1204847\n2160216\n248206\n")
    w = io.StringIO()
    netflix_solve(r, w)
    self.assertEqual(w.getvalue(), "10007:\n3.7\n3.7\n3.7\nRMSE: 1.7767010628315238\n")

  # ---
  # netflix_predict
  # ---
  def test_predict(self) :
    prediction = netflix_predict(1, (4,8,10,12))
    self.assertEqual(prediction.movie, 1)
    self.assertEqual(prediction.predictions, 4 * [3.7])

  def test_predict2(self) :
    prediction = netflix_predict(2, (1,2,3,4))
    s = io.StringIO()
    self.assertEqual(prediction.movie, 2)
    prediction.display(s)
    self.assertEqual(s.getvalue(), "2:\n3.7\n3.7\n3.7\n3.7\n")

  def test_predict3(self) :
    prediction = netflix_predict(1, (1,2,3))
    self.assertTrue(type(prediction), Prediction)

  def test_prediction_display(self) :
    prediction = Prediction(3, [5,6,7], [3.42, 4.21, 2.18])
    s = io.StringIO()
    prediction.display(s)
    self.assertEqual(s.getvalue(), "3:\n3.4\n4.2\n2.2\n")

  def test_prediction_display2(self) :
    prediction = Prediction(2, [1,2], [2,3])
    s = io.StringIO()
    prediction.display(s)
    self.assertEqual(s.getvalue(), "2:\n2\n3\n")

  def test_prediction_rmse(self) :
    set_cache_probe({1: {1: 3, 4:2, 5:5}})
    prediction = Prediction(1, [1,4,5], [3.7, 2.1, 4.2])
    r = prediction.calculate_rmse()
    set_cache_probe(None)
    self.assertEqual(r, 0.6164414002968976)

  def test_prediction_rmse2(self) :
    set_cache_probe({1: {1: 3, 4:2, 5:5}})
    prediction = Prediction(1, [1,4,5], [3, 2, 5])
    r = prediction.calculate_rmse()
    set_cache_probe(None)
    self.assertEqual(r, 0.0)


  # ---
  # netflix_load_cache
  # ---

  def test_load_cache(self) :
    cache = netflix_load_cache(CACHE_PROBE, "word-probeMapCache.txt")
    self.assertEqual(len(cache[10]), 2)
    self.assertEqual(cache[10][1531863], 3)

  def test_load_cache2(self) :
    cache = netflix_load_cache(CACHE_GENERAL, "irvin-movie_avg_rating.txt")
    self.assertEqual(len(cache), 17770)
    self.assertEqual(cache[872], 4.199615032659114)
    self.assertEqual(cache[14683], 3.7777777777777777)

  def test_load_cache3(self) :
    cache = netflix_load_cache(CACHE_GENERAL, "ericweb2-movieAveragesOneLine.txt")
    self.assertEqual(len(cache), 17770)
    self.assertEqual(cache[4863], 3.0)
    self.assertEqual(cache[5267], 3.395734597156398)

  def test_get_cache_probe(self) :
    cache = get_cache_probe()
    self.assertEqual(len(cache[10]), 2)
    self.assertEqual(cache[10][1531863], 3)

  # ---
  # rmse
  # ---
  def test_rmse1 (self) :
    a = (2,3,4)
    b = (2,3,4)
    self.assertTrue(str(rmse(a,b)) == "0.0")
  
  def test_rmse2 (self) :
    a = [2,3,4]
    b = (3,4,5)
    self.assertTrue(str(rmse(a,b)) == "1.0")
    self.assertTrue(str(rmse(b,a)) == "1.0")

  def test_rmse3 (self) :
    a = (1,4,5,8,9)
    b = (1,5,5,4,8)
    self.assertTrue(str(round(rmse(a,b), 6)) == "1.897367")

  def test_rmse4 (self) :
    a = 1000000 * [1]
    b = 1000000 * [6]
    self.assertTrue(str(rmse(a,b)) == "5.0")

print("TestNetflix.py")
unittest.main()
print("Done.")