#!/usr/bin/env python
import sys
sys.path.append('..')
from reportlab_goldstandard import generate
from bill import Bill
""" test_rp_gs.py: This module invokes the gold standard generator with some
                   simple input in order to do a first level sanity check
                   of the output.
"""

gs = generate.Goldstandard(title="SENATE SESSION - Thursday March 10, 2016",\
                           filename="test_simple_gs.pdf")
Bill1=Bill("HB 101","a bill that does bad things. Don't be" +'"surprised"',
           "evil committee", "OTP 3-1",\
           "ANTI-LIBERTY", "It really does bad things" +\
           'and some "double quotes"',
           "NAY OTP", \
           "* Does lots of bad things.\n * Even worse than you think.\n" +\
           " * Stop doing that")

Bill2=Bill("SB 121","a bill that does good things", "Ice Cream committee", \
           "OTP 9-1", "PRO-LIBERTY", "It really does good things",
           "YEA OTP", "* Does of good things.\n "+\
           "* Even Better than you think.\n * Don't Don't " + '"Double Quote"')

gs.Set_Bills([Bill1, Bill2, Bill1, Bill2, Bill1, Bill2, Bill1, Bill2])
gs.save()
