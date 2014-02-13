#!/usr/bin/env python3

"""
To test the program:
    % python TestNetflix.py > TestNetflix.out
    % chmod ugo+x TestNetflix.py
    % TestNetflix.py > TestNetflix.out
"""

import io
import unittest

from Netflix import netflix_solve, rmse, netflix_load_cache, CACHE_PROBE, CACHE_GENERAL

class TestNetflix (unittest.TestCase) :
  # ---
  # netflix_solve
  # ---
  def test_solve1 (self) :
    r = io.StringIO("1:\n14756\n")
    w = io.StringIO()
    netflix_solve(r, w)
    self.assertTrue(w.getvalue() == "1:\n3.7\n")

  def test_solve2 (self) :
    r = io.StringIO("1:\n712610\n1772839\n1059319\n2380848\n548064\n")
    w = io.StringIO()
    netflix_solve(r, w)
    self.assertTrue(w.getvalue() == "1:\n3.7\n3.7\n3.7\n3.7\n3.7\n")

  def test_solve3 (self) :
    r = io.StringIO("10007:\n1204847\n2160216\n248206\n")
    w = io.StringIO()
    netflix_solve(r, w)
    self.assertTrue(w.getvalue() == "10007:\n3.7\n3.7\n3.7\n")

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