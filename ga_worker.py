import random
import bbobbenchmarks as bn
import uuid
import os

from deap import base
from deap import creator
from deap import tools
from evospace import EvoSpace

class GA_Worker:
    def __init__(self, conf):
        self.conf = conf
        self.function = bn.dictbbob[self.conf['function']](int(self.conf['instance']))
        self.F_opt = self.function.getfopt()
        self.function_evaluations = 0 #Is not needed in EvoWorkers, they dont know the number of FE
        self.maximum_function_evaluations = self.conf['FEmax'] #Is not needed in EvoWorkers, they dont know the number of FE
        self.deltaftarget = 1e-8
        self.toolbox = base.Toolbox()
        self.FC = 0
        self.worker_uuid = uuid.uuid1()
        self.space = EvoSpace(self.conf['evospace_url'], self.conf['pop_name'])
        self.params = None
        self.evospace_sample = None

    def setup(self):
        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))     #Minimizing Negative
        creator.create("Individual", list, typecode='d', fitness=creator.FitnessMin)
        self.toolbox = base.Toolbox()
        self.toolbox.register("attr_float", random.uniform, -5, 5)
        self.toolbox.register("individual", tools.initRepeat, creator.Individual,
                              self.toolbox.attr_float, self.conf['dim'])
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)
        self.toolbox.register("evaluate", self.eval)
        self.toolbox.register("mate", tools.cxTwoPoint)
        self.toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=0.5, indpb=0.05)
        self.toolbox.register("select", tools.selTournament, tournsize=12)

    def eval(self, individual):
        return  self.function(individual),

    def initialize(self,n=300):
        self.space.delete()
        self.space.initialize()
        pop = self.toolbox.population(n)
        init_pop = [{"chromosome": ind[:], "id": None, "fitness": {"DefaultContext": 0.0}} for ind in pop]
        self.space.post_subpop(init_pop)

    def get(self):
        self.evospace_sample = self.space.get_sample(self.conf['sample_size'])
        #If the individual has been evaluated before, assign the fitness so is not evaluated again


        pop = []
        for cs in self.evospace_sample['sample']:
            ind = creator.Individual(cs['chromosome'])
            if 'score' in cs['fitness']:
               ind.fitness =  creator.FitnessMin(values=(cs['fitness']['score'] ,))
            pop.append(ind)

        return pop

    def put_back(self,pop):
        final_pop = [{"chromosome": ind[:], "id": None,
                      "fitness": {"DefaultContext": ind.fitness.values[0], "score": ind.fitness.values[0]}} for ind in
                     pop]

        self.evospace_sample['sample'] = final_pop

        if 'benchmark' in self.conf:
            experiment_id = 'experiment_id' in conf and conf['experiment_id'] or 0
            self.evospace_sample['benchmark_data'] = {'params': self.params, 'evals': evals, 'algorithm': 'GA',
                                                 'benchmark': self.conf['function'], 'instance': self.conf['instance'],
                                                 'worker_id': str(self.worker_uuid), 'experiment_id': experiment_id,
                                                 'dim':self.conf['dim'],
                                                 'fopt': self.function.getfopt() }
        self.space.put_sample(self.evospace_sample)

    def run(self, pop):
        evals = []
        num_fe_first_sample = 0
        first_sample = True

        #random.seed(i)
        CXPB, MUTPB, NGEN = random.uniform(.8,1), random.uniform(.1,.6), conf['NGEN']



        # Evaluate the entire population

        invalid_ind = [ind for ind in pop if not ind.fitness.valid]
        num_fe_first_sample += len(invalid_ind)

        fitnesses = list(map(self.toolbox.evaluate, pop))
        for ind, fit in zip(pop, fitnesses):
            ind.fitness.values = fit

        # print("  Evaluated %i individuals" % len(pop))
        self.params = { 'CXPB':CXPB,'MUTPB':MUTPB, 'NGEN' : NGEN, 'sample_size': self.conf['sample_size'],
                   'crossover':'cxTwoPoint', 'mutation':'mutGaussian, mu=0, sigma=0.5, indpb=0.05',
                   'selection':'tools.selTournament, tournsize=12','init':'random:[-5,5]'
                   }

        # Begin the evolution
        for g in range(NGEN):
            num_fe = 0

            if first_sample:
                first_sample = False
                num_fe+=num_fe_first_sample


            #print("-- Generation %i --" % g)

            # Select the next generation individuals
            offspring = self.toolbox.select(pop, len(pop))
            # Clone the selected individuals
            offspring = list(map(self.toolbox.clone, offspring))

            # Apply crossover and mutation on the offspring
            for child1, child2 in zip(offspring[::2], offspring[1::2]):

                # cross two individuals with probability CXPB
                if random.random() < CXPB:
                    self.toolbox.mate(child1, child2)

                    # fitness values of the children
                    # must be recalculated later
                    del child1.fitness.values
                    del child2.fitness.values

            for mutant in offspring:

                # mutate an individual with probability MUTPB
                if random.random() < MUTPB:
                    self.toolbox.mutate(mutant)
                    del mutant.fitness.values

            # Evaluate the individuals with an invalid fitness
            invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
            fitnesses = map(self.toolbox.evaluate, invalid_ind)
            for ind, fit in zip(invalid_ind, fitnesses):
                ind.fitness.values = fit

            #print("  Evaluated %i individuals" % len(invalid_ind))
            num_fe = num_fe + len(invalid_ind)

            # The population is entirely replaced by the offspring
            pop[:] = offspring

            # Gather all the fitnesses in one list and print the stats
            fits = [ind.fitness.values[0] for ind in pop]
            evals.append((g, min(fits),tools.selBest(pop, 1)[0], num_fe ))


        best_ind = tools.selBest(pop, 1)[0]
        if (best_ind.fitness.values[0] <= self.function.getfopt() + 1e-8) or self.FC >= self.maximum_function_evaluations:
            return True, evals,  pop, best_ind
        else:
            return False,evals,  pop,  best_ind

if __name__ == "__main__":

    conf = {}
    conf['function'] = 'FUNCTION' in os.environ and int(os.environ['FUNCTION']) or  3
    conf['instance'] = 'INSTANCE' in os.environ and int(os.environ['INSTANCE']) or  1
    conf['dim'] = 'DIM' in os.environ and int(os.environ['DIM']) or  5
    conf['sample_size'] = 'SAMPLE_SIZE' in os.environ and int(os.environ['SAMPLE_SIZE']) or 300
    conf['FEmax'] = 500000
    conf['evospace_url'] = 'EVOSPACE_URL' in os.environ and os.environ['EVOSPACE_URL'] or '127.0.0.1:3000/evospace'
    conf['pop_name'] = 'POP_NAME' in os.environ and os.environ['POP_NAME'] or 'test_pop'
    conf['max_samples'] = 'MAX_SAMPLES' in os.environ and int(os.environ['MAX_SAMPLES']) or 22
    conf['benchmark'] = 'BENCHMARK' in os.environ
    conf['NGEN'] = 'NGEN' in os.environ and int(os.environ['NGEN']) or 20
    conf['experiment_id'] = 'EXPERIMENT_ID' in os.environ and int(os.environ['EXPERIMENT_ID']) or str(uuid.uuid1())

    worker = GA_Worker(conf)

    worker.setup()


    #worker.initialize(200)
    for i  in range(conf['max_samples']):
        print i ,

        pop = worker.get()
        finished, evals,  pop,  best_ind = worker.run(pop)
        print evals
        print conf['function'],conf['instance'],  worker.function.getfopt(),  best_ind.fitness.values[0],  '%+10.9e'% (best_ind.fitness.values[0] - worker.function.getfopt() + 1e-8)
        worker.put_back(pop)

        #Run to the end if benchmark
        if finished and not conf['benchmark']:
            break

