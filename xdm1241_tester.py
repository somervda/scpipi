#!/usr/bin/python3

# Turn on and plug in xdm1241 before running this
# it should complete withot errors

from xdm1241 import Xdm1241

# Make a xdm1241 object
o = Xdm1241(quiet=False)

assert o.isConnected() == False , "xdm1241 should be disconnected"
assert o.type == "" , "type should be blank"
assert o.range == "" , "range should be blank"
assert o.rate == "" , "rate should be blank"

assert o.connect() == True , "xdm1241 should connect"
assert o.isConnected() == True , "xdm1241 should be connected"

assert o.configure("voltdc",0,0) == True , "xdm1241 configure should work"

assert o.measure() != False , "xdm1241 measure should work"

assert o.type == "voltdc" , "type should be voltdc"
assert o.range == 0 , "range should be 0"
assert o.rate == 0 , "rate should be 0"