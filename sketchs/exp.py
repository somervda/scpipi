import math

def fexp(f):
    return int(math.floor(math.log10(abs(f)))) if f != 0 else 0

def fman(f):
    return f/10**fexp(f)

value = .00134
exponent= fexp(value)
mantisa= fman(value)
print(value,mantisa,exponent)
if mantisa<2:
    mantisa = 2
elif mantisa<5:
    mantisa=5
else:
    mantisa=1
    exponent+=1
result= mantisa * 10**exponent
print(exponent,mantisa,result)


