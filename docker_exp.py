
import time
import os
import docker_worker as dw
import evospace
import json



#Set IP of REDIS box. Redis Host is sent to workers so it can not be 127.0.0.1
REDIS_HOST= 'REDIS_HOST' in os.environ and int(os.environ['REDIS_HOST']) or '192.168.1.13'
#Experiment ID must be an integer
EXPERIMENT_ID = 107

DATA_ROOT = './experiment_data'
DATA_FOLDER = './experiment_data/' + str(EXPERIMENT_ID)


for dim in (2,3):
#for dim in (2, 3, 5, 10):
    print "DIM", dim

    #for instance in range(1,6)+range(41, 51):
    for instance in range(1,3):
        print "instance", instance
        EVOSPACE_SIZE = 100
        env = {'FUNCTION': 3, 'DIM': dim, 'INSTANCE': instance,  'FEmax': 500000,
               'EVOSPACE_URL': REDIS_HOST + ':3000/evospace', 'POP_NAME': 'test_pop',
               'UPPER_BOUND': 5, 'LOWER_BOUND': -5, 'BENCHMARK': True, 'EXPERIMENT_ID': EXPERIMENT_ID,
               'NGEN': 10, 'SAMPLE_SIZE': 20, 'MAX_SAMPLES': 5, 'BENCHMARK': True}

        info = {'workers': {'GA': {'Number': 1, 'envs': [env]}, 'PSO': {'Number': 1, 'envs': [env]}}}

        print "initializing space"
        evospace.initialize(REDIS_HOST + ':3000/evospace','test_pop',env['DIM'],-5,5,EVOSPACE_SIZE)
        print dw.get_containers()
        dw.kill_all()
        dw.remove_all()


        try:
            os.makedirs(DATA_FOLDER)
        except OSError:
            pass

        with open(DATA_FOLDER+'/info_'+str(EXPERIMENT_ID)+'.json', 'w') as f:
            json.dump({'info':info}, f)

        gas =  [dw.make_container(env, "python /home/EvoWorker/ga_worker.py %s ") for _ in range(1) ]
        psos = [dw.make_container(env, "python /home/EvoWorker/pso_worker.py %s ") for _ in range(1)]
        containers = gas+psos

        for c in containers:
            "Starting",c
            c.start()

        while True:
            time.sleep(1)

            if( dw.dC.containers.list(filters={'label':'evo_worker'})):
                print ".",
            else:
                print "Finished"
                for c in containers:
                    print c.logs()
                break


