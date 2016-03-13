#!/usr/bin/env python
from opendoc_goldstandard import Opendoc_Goldstandard
from bill import Bill

gs = Opendoc_Goldstandard()
Bill1=Bill("HB 101","a bill that does bad things", "evil committe", "OTP 3-1", "ANTI-LIBERTY", "It really does bad things",
"NAY OTP", "* Does lots of bad things.\n * Even worse than you think.\n * Stop doing that")
Bill2=Bill("SB 121","a bill that does good things", "ice cream committe", "OTP 9-1", "PRO-LIBERTY", "It really does good things",
"YEA OTP", "* Does loots of good things.\n * Even Better than you think.\n * More of this ") 
gs.Set_Bills([Bill1, Bill2])
gs.save("standard.odt")
