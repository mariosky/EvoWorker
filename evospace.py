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

    def post_subpop(self, pop):
        ind = {'sample':pop}
        r = requests.post(self.url+'sample', json=ind)
        return r.text

    def put_sample(self,pop):
        r = requests.put(self.url+'sample', json=pop)
        return r.text

    def get_sample(self,n):
        if isinstance(n, int):
            n = str(n)
        r = requests.get(self.url + 'sample/'+ n)
        return r.json()['result']


def initialize( evospace_url, pop_name, dim, lb, ub, n ):
    space = EvoSpace(evospace_url, pop_name)
    space.delete()
    space.initialize()
    init_pop = [{"chromosome": [random.uniform(lb,ub) for _ in range(dim)], "id": None, "fitness": {"DefaultContext": 0.0}} for _ in range(n)]
    space.post_subpop(init_pop)






