
HOST="127.0.0.1"
PORT=6379

import urlparse, ast
import os, redis, json
from CoCo import CoCoData
from itertools import groupby
from operator import itemgetter


if os.environ.get('REDISTOGO_URL'):
    url = urlparse.urlparse(os.environ.get('REDISTOGO_URL'))
    r = redis.Redis(host=url.hostname, port=url.port, password=url.password)
#LOCAL
else:
    r = redis.Redis(host=HOST, port=PORT)


EXPERIMENT_ID = 80
DATA_FOLDER = './experiment_data/' + str(EXPERIMENT_ID) + '/'
experiment = 'log:test_pop:' + str(EXPERIMENT_ID)

data = [ast.literal_eval(i) for i in r.lrange(experiment, 0, -1)]
data.reverse()

#IF not exisits
try:
    os.makedirs(DATA_FOLDER)
except OSError:
    pass
with open(DATA_FOLDER+experiment+'.json', 'w') as f:
    json.dump(data, f)


grp_benchmark = itemgetter("benchmark")
grp_instance = itemgetter("benchmark","instance")
result = []
for key, benchmark_group in groupby(data, grp_benchmark):
    print key
    for key,benchmark in groupby(benchmark_group, grp_instance):
        print key
        coco = CoCoData(5)
        index = 0
        total = 0
        result = []
        for row in benchmark:
            data_row = []
            row_id=0
            for e in row['evals']:
                data_row.append((e[1], row['algorithm'], e[0],row['params']['sample_size'], e[1],row['fopt'], '%+10.9e'% ( e[1]-row['fopt']),e[2]))
                row_id+=1
            data_row.sort(reverse=True)
            for r in data_row:
                coco.evalfun(*r[1:],result=result)
        print result

