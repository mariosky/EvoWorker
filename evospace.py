import requests
import random

class Individual:
    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.fitness = kwargs.get('fitness',{})
        self.chromosome = kwargs.get('chromosome',[])
        self.__dict__.update(kwargs)

    def __repr__(self):
        return self.id +":"+ str(self.fitness) +":" + str( self.chromosome)

    def as_dict(self):
        return self.__dict__

    def chromosome_map(self, f):
        return map(f,self.chromosome)




class EvoSpace(object):
    def __init__(self, server, space):
        self.server = server
        self.space = space
        self.url = 'http://%s/%s/'%(self.server,self.space)

    def delete(self):
        requests.delete(self.url)

    def initialize(self):
        requests.post(self.url+'initialize')

    def post_individual(self,individual):
        requests.post(self.url+'individual', data=individual)

    def get__individual(self, id ):
        if isinstance(id,int):
            id = str(id)
        r = requests.get(self.url+'individual/'+id)
        return Individual(**r.json())










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

