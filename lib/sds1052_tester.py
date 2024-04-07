#!/usr/bin/python3

# Turn on and plug in sds1052 before running this
# it should complete withot errors

from sds1052 import Sds1052

# Make a sds1052 object
o = Sds1052(quiet=True)

assert o.isConnected() == False , "sds1052 should be disconnected"
assert o.connect() == True , "sds1052 should connect"
assert o.isConnected() == True , "sds1052 should be connected"
assert o.measure("RMS")["success"] == True , "sds1052 measure  should work"