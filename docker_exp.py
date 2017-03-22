

import docker
from deap import base

import os

import time
import random
from evospace import EvoSpace

import sys, getopt


ALGORITHMS = ["ga","gwo","pso"]


dC = docker.DockerClient(base_url='unix://var/run/docker.sock', version="auto", timeout=60)
BASE_IMAGE = 'mariosky/evo_worker:latest'


def create_worker(env, command):
    # TODO catch ContainerError - requests.exceptions.ConnectionError
    container = make_container(env, command=command)
    start(container)
    return container


class ContainerException(Exception):
    """
    There was some problem generating or launching a docker container
    for the user
    """
    pass


class ImageException(Exception):
    """
    There was some problem reading image
    """
    pass



def make_container(env, command = "python /home/EvoWorker/ga_worker.py %s " ):
    return dC.containers.create(BASE_IMAGE, environment=env ,command=command,  labels={'evo_worker':'ga' })


def start(cont):
    dC.start(cont['Id'])



def kill_all():
    for container in get_containers('evo_worker'):
        print "Killing: ", container
        container.kill()


def remove_all():
    for container in get_containers(all=True):
        print "Removing: ", container
        container.remove(force=True)


def get_containers(label='evo_worker', all=False):
    return dC.containers.list(all=all, filters={'label': label})


def initialize( evospace_url, pop_name, dim, lb, ub, n ):
    space = EvoSpace(evospace_url, pop_name)
    space.delete()
    space.initialize()
    init_pop = [{"chromosome": [random.uniform(lb,ub) for _ in range(dim)], "id": None, "fitness": {"DefaultContext": 0.0}} for _ in range(n)]
    space.post_subpop(init_pop)




if __name__ == "__main__":
    print "clearing space"
    initialize('192.168.1.100:3000/evospace','test_pop',5,-5,5,1000)
    time.sleep(20)
    print get_containers()
    print  kill_all()


    remove_all()



    env = { 'FUNCTION': 3, 'INSTANCE':1, 'DIM':5,'FEmax':500000,
               'EVOSPACE_URL': '192.168.1.100:3000/evospace','POP_NAME':  'test_pop',
               'UPPER_BOUND': 5, 'LOWER_BOUND': -5,  'BENCHMARK': True, 'EXPERIMENT_ID': 55,

               'NGEN': 50, 'SAMPLE_SIZE':100, 'MAX_SAMPLES':10,'BENCHMARK':True}

    #gwo_env = {'FUNCTION': 3, 'INSTANCE': 1, 'DIM': 5, 'FEmax': 500000,
    #           'EVOSPACE_URL': '192.168.1.100:3000/evospace', 'POP_NAME': 'test_pop',
    #           'UPPER_BOUND': 5, 'LOWER_BOUND': -5,  'BENCHMARK': True, 'EXPERIMENT_ID': 12,

    #          'SAMPLE_SIZE': 100, 'MAX_SAMPLES': 22,  'NGEN': 10}

    #pso_env = {'FUNCTION': 3, 'INSTANCE': 1, 'DIM': 5, 'FEmax': 500000,
    #           'EVOSPACE_URL': '192.168.1.100:3000/evospace', 'POP_NAME': 'test_pop',
    #           'UPPER_BOUND': 5, 'LOWER_BOUND': -5, 'BENCHMARK': True, 'EXPERIMENT_ID': 12,
#
 #              'SAMPLE_SIZE': 100, 'MAX_SAMPLES': 40, 'NGEN': 50}

  #  algs = [ (gwo_env,"python /home/EvoWorker/gwo_worker.py %s "),
   #          (ga_env, "python /home/EvoWorker/ga_worker.py %s "),
    #         (pso_env, "python /home/EvoWorker/pso_worker.py %s "),
     #       ]

    #gwo = make_container(gwo_env,"python /home/EvoWorker/gwo_worker.py %s ")
    #ga =  make_container(ga_env, "python /home/EvoWorker/ga_worker.py %s ")
    #pso = make_container(pso_env, "python /home/EvoWorker/pso_worker.py %s ")
    #containers = [ga, pso]

    gas =  [make_container(env, "python /home/EvoWorker/ga_worker.py %s ") for _ in range(2) ]
    psos = [make_container(env, "python /home/EvoWorker/pso_worker.py %s ") for _ in range(2)]
    containers = psos+gas
    #containers = gas+psos





    time.sleep(10)
    for c in containers:
        "start",c
        c.start()


    while True:
        time.sleep(3)
        if( dC.containers.list(filters={'label':'evo_worker'})):
            print "Working"
        else:
            print "Bye"
            #print gwo.logs()
            #print ga.logs()
            #print pso.logs()
            for c in containers:
                print c.logs()
            break


    # for a in ALGORITHMS:
    #
    #     print create_worker({'LANG':cola.app_name, 'REDIS_HOST':os.environ['REDIS_HOST'], 'REDIS_PORT':os.environ['REDIS_PORT']})
    #
    #     print create_worker({'LANG':cola.app_name, 'REDIS_HOST':os.environ['REDIS_HOST'], 'REDIS_PORT':os.environ['REDIS_PORT']})
    #
    #     time.sleep(4)
    #
    #
    # while True:
    #     time.sleep(1)
    #     containers = get_containers()
    #     workers = [ w.split(':worker:') for w in Cola.get_all_workers()]
    #     for c_lang, c_id in containers:
    #
    #
    #         if c_id not in [w_id for w_lang, w_id  in workers]:
    #             print "Killing: ", c_id, c_lang
    #             dC.kill(c_id)
    #             dC.remove_container(c_id)
    #             print "Removing: ", c_id
    #             print create_worker({'LANG':c_lang, 'REDIS_HOST':os.environ['REDIS_HOST'], 'REDIS_PORT':os.environ['REDIS_PORT']})
