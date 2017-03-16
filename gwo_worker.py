import random
import bbobbenchmarks as bn
import uuid
import os
import numpy as np

from EvoloPy import GWO as gwo

from evospace import EvoSpace

class GWO_Worker:
    def __init__(self, conf):
        self.conf = conf
        self.function = bn.dictbbob[self.conf['function']](self.conf['instance'])
        self.F_opt = self.function.getfopt()
        self.function_evaluations = 0
        self.maximum_function_evaluations = self.conf['FEmax']
        self.deltaftarget = 1e-8
        self.FC = 0
        self.worker_uuid = uuid.uuid1()

        self.space = EvoSpace(self.conf['evospace_url'], self.conf['pop_name'])

        self.evospace_sample = None

    def setup(self):
        pass
        #evospace_sample = self.space.get_sample(self.conf['sample_size'])

    def get(self):
        self.evospace_sample = self.space.get_sample(self.conf['sample_size'])
        pop = [cs['chromosome'] for cs in self.evospace_sample['sample']]
        return np.array(pop)


    def run(self, pop):
        self.function.__name__ = "F%s instance %s" % (self.conf['function'], self.conf['instance'])
        gwo.GWO(objf=self.function, lb=conf['lb'], ub=conf['ub'], dim=self.conf['dim'], SearchAgents_no=conf['sample_size'], Max_iter=conf['NGEN'], Positions=pop)


if __name__ == "__main__":
    conf = {}
    conf['function'] = 3
    conf['instance'] = 1
    conf['dim'] = 5
    conf['sample_size'] = 5
    conf['FEmax'] = 500000
    conf['evospace_url'] = 'EVOSPACE_URL' in os.environ and os.environ['EVOSPACE_URL'] or '127.0.0.1:3000/evospace'
    conf['pop_name'] = 'POP_NAME' in os.environ and os.environ['POP_NAME'] or 'test_pop'
    conf['max_samples'] = 'MAX_SAMPLES' in os.environ and int(os.environ['MAX_SAMPLES']) or 1
    conf['benchmark'] = 'BENCHMARK' in os.environ
    conf['experiment_id'] = 'EXPERIMENT_ID' in os.environ and int(os.environ['EXPERIMENT_ID']) or str(uuid.uuid1())
    conf['lb'] = 'LOWER_BOUND' in os.environ and int(os.environ['LOWER_BOUND']) or -5
    conf['ub'] = 'UPPER_BOUND' in os.environ and int(os.environ['UPPER_BOUND']) or 5
    conf['NGEN'] = 'NGEN' in os.environ and int(os.environ['NGEN']) or  10


    worker = GWO_Worker(conf)
    pop = worker.get()
    print "Ready"
    for i  in range(conf['max_samples']):
        print i ,
        print worker.run(pop)


#    for i in range(conf['max_samples']):
#        print i,
#        pop = worker.get()
#        finished, evals, pop, best_ind = worker.run(pop)
#        print   best_ind.fitness.values[0], '%+10.9e' % (best_ind.fitness.values[0] - worker.function.getfopt() + 1e-8)
#        worker.put_back(pop)
#        if finished:
#            break
