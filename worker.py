import bbobbenchmarks as bn
import uuid
import os
import numpy as np

from evospace import EvoSpace

class Worker(object):
    def __init__(self, conf):
        self.conf = conf
        self.function = bn.dictbbob[self.conf['function']](self.conf['instance'])
        self.F_opt = self.function.getfopt()
        self.function_evaluations = 0
        self.maximum_function_evaluations = self.conf['FEmax']
        self.deltaftarget = 1e-8
        self.FC = 0
        self.worker_uuid = uuid.uuid1()
        self.params = None

        self.space = EvoSpace(self.conf['evospace_url'], self.conf['pop_name'])
        self.evospace_sample = None

    def setup(self):
        raise NotImplementedError("Please Implement this method")

    def get(self):
        self.evospace_sample = self.space.get_sample(self.conf['sample_size'])
        pop = [cs['chromosome'] for cs in self.evospace_sample['sample']]
        return np.array(pop)

    def put_back(self, s):
        raise NotImplementedError("Please Implement this method")

    def run(self, pop):
        raise NotImplementedError("Please Implement this method")

