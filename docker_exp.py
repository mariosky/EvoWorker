
import time
import os
import docker_worker as dw
import evospace
import json



#Set IP of REDIS box. Redis Host is sent to workers so it can not be 127.0.0.1
REDIS_HOST= 'REDIS_HOST' in os.environ and os.environ['REDIS_HOST'] or '192.168.1.102'
#Experiment ID must be an integer
EXPERIMENT_ID = 10444

DATA_ROOT = './experiment_data'
DATA_FOLDER = './experiment_data/' + str(EXPERIMENT_ID)


es_conf = {
    2: {'EVOSPACE_SIZE':250, 'NGEN':50, 'SAMPLE_SIZE': 100, 'MAX_SAMPLES':20, 'PSO':1, 'GA':1 },
    3: {'EVOSPACE_SIZE':250, 'NGEN':50, 'SAMPLE_SIZE': 100, 'MAX_SAMPLES':30, 'PSO':1, 'GA':1 },
    5: {'EVOSPACE_SIZE':500, 'NGEN':50, 'SAMPLE_SIZE': 100, 'MAX_SAMPLES':25, 'PSO':2, 'GA':2 },
    10:{'EVOSPACE_SIZE':1000,'NGEN':50, 'SAMPLE_SIZE': 200, 'MAX_SAMPLES':25, 'PSO':2, 'GA':2 },
    20:{'EVOSPACE_SIZE':2000,'NGEN':50, 'SAMPLE_SIZE': 200, 'MAX_SAMPLES':25, 'PSO':4, 'GA':4 },
    40:{'EVOSPACE_SIZE':4000,'NGEN':50, 'SAMPLE_SIZE': 200, 'MAX_SAMPLES':25, 'PSO':8, 'GA':8 },
}


for function in (2):

    for dim in (2,20):
        print "DIM", dim
        print "instance:",

        for instance in range(1,6)+range(41, 51):
        #for instance in range(1,3):

            print instance,

            env = {'FUNCTION': function, 'DIM': dim, 'INSTANCE': instance,  'FEmax': 500000,
                   'EVOSPACE_URL': REDIS_HOST + ':3000/evospace', 'POP_NAME': 'test_pop',
                   'UPPER_BOUND': 5, 'LOWER_BOUND': -5, 'BENCHMARK': True, 'EXPERIMENT_ID': EXPERIMENT_ID,
                   'NGEN': es_conf[dim]['NGEN'], 'SAMPLE_SIZE': es_conf[dim]['SAMPLE_SIZE'],
                   'MAX_SAMPLES': es_conf[dim]['MAX_SAMPLES'], 'BENCHMARK': True}

            info = {'workers': {'GA': {'Number': 1, 'envs': [env]}, 'PSO': {'Number': 1, 'envs': [env]}}}

            #print "initializing space"
            evospace.initialize(REDIS_HOST + ':3000/evospace','test_pop',env['DIM'],-5,5, es_conf[dim]['EVOSPACE_SIZE'])
            #print dw.get_containers()
            dw.kill_all()
            dw.remove_all()


            try:
                os.makedirs(DATA_FOLDER)
            except OSError:
                pass

            with open(DATA_FOLDER+'/info_'+str(EXPERIMENT_ID)+'.json', 'w') as f:
                json.dump({'info':info}, f)

            gas =  [dw.make_container(env, "python /home/EvoWorker/ga_worker.py %s ") for _ in range(es_conf[dim]['GA']) ]
            psos = [dw.make_container(env, "python /home/EvoWorker/pso_worker.py %s ") for _ in range(es_conf[dim]['PSO'])]
            containers = gas+psos

            for c in containers:
                "Starting",c
                c.start()

            while True:
                time.sleep(1)

                if( dw.dC.containers.list(filters={'label':'evo_worker'})):
                    #print ".",
                    pass
                else:
                    print "F",
                    for c in containers:
                        pass
                        #print c.logs()
                    break


