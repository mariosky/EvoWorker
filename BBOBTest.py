import bbobbenchmarks as bn
for s in bn.nfreeinfos:
    print s

f1 = bn.F1(1)

print  f1(range(10))
print f1.getfopt()

print f1

i =  bn.instantiate(1)

print i
