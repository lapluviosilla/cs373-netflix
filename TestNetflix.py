#!/usr/bin/env python3

"""
To test the program:
    % python TestNetflix.py > TestNetflix.out
    % chmod ugo+x TestNetflix.py
    % TestNetflix.py > TestNetflix.out
"""

import io
import unittest

from Netflix import netflix_solve, rmse

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