#!/usr/bin/env python3
# Paul Strong
# 
"""
To test the program:
    % python TestNetflix.py > TestNetflix.out
    % chmod ugo+x TestNetflix.py
    % TestNetflix.py > TestNetflix.out
"""

import sys

from Netflix import netflix_solve

netflix_solve(sys.stdin, sys.stdout)