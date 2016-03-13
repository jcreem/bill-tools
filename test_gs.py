#!/usr/bin/env python
from opendoc_goldstandard import Opendoc_Goldstandard
from bill import Bill

gs = Opendoc_Goldstandard()
Bill1=Bill("HB 101","a bill that does bad things", "evil committe", "ITL 3-1", 
gs.save("standard.odt")
