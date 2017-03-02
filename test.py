
from evospace import *

evo = EvoSpace('127.0.0.1:3000/evospace','test_pop')
evo.delete()
evo.post_individual( {'id':'id:3:2', 'name':"Mario", 'chromosome':[1,2,3,1,1,2,2,2],"fitness":{"s":1},"score":random.randint(1,1000) })
evo.post_individual( { 'name':"Mario", 'chromosome':[2,2,3,1,1,2,2,2],"fitness":{"s":10},"score":random.randint(1,1000)})

for i in range(10):
    ind = { 'name':"Mario", 'chromosome':[2,2,3,1,1,2,2,2],"fitness":{"s":i},"score":random.randint(1,1000)}
    evo.post_individual(ind)



print evo.url
ind =  evo.get__individual(3)

print ind.chromosome_map(int)