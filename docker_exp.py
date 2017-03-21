

import docker
import os

import time
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





if __name__ == "__main__":
    print get_containers()
    print  kill_all()

    remove_all()

    env = {}
    env['FUNCTION'] = 3
    env['INSTANCE'] =  1
    env['DIM'] = 'DIM' in os.environ and os.environ['DIM'] or  5
    env['SAMPLE_SIZE'] = 'SAMPLE_SIZE' in os.environ and os.environ['SAMPLE_SIZE'] or 300
    env['FEmax'] = 500000
    env['EVOSPACE_URL'] = '192.168.1.100:3000/evospace'
    env['POP_NAME'] = 'test_pop'
    env['MAX_SAMPLES'] =  22
    env['BENCHMARK'] = True
    env['EXPERIMENT_ID'] = 12

    c = make_container(env)
    c.start()
    while True:
        time.sleep(3)
        if( dC.containers.list(filters={'label':'evo_worker'})):
            print "Working"
        else:
            print "Bye"
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
