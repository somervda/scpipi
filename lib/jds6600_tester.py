#!/usr/bin/python3

# Turn on and plug in jds6600 before running this
# it should complete withot errors

from jds6600 import Jds6600

# Make a jds6600 object
o = Jds6600(quiet=False)

assert o.isConnected() == False , "jds6600 should be disconnected"
assert o.connect() == True , "jds6600 should connect"
assert o.isConnected() == True , "jds6600 should be connected"

assert o.configure(300010,2.2,1)== True , "jds6600 configure should work"

