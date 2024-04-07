#!/usr/bin/python3

# Turn on and plug in dho804 before running this
# it should complete withot errors

from dho804 import Dho804

# Make a dho804 object
o = Dho804(quiet=True)

assert o.isConnected() == False , "dho804 should be disconnected"
assert o.connect() == True , "dho804 should connect"
assert o.isConnected() == True , "dho804 should be connected"
assert o.measure("VPP")["success"] == True , "dho804 measure  should work"
