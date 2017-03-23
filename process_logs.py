
HOST="127.0.0.1"
PORT=6379
##REDISCLOUD
import urlparse, ast

import os, redis, json

from CoCo import CoCoData

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



from itertools import groupby
from operator import itemgetter

grouper = itemgetter("benchmark", "instance")
result = []
for key, grp in groupby(data, grouper):
    print key
    coco = CoCoData(5)
    index = 0
    total = 0
    result = []
    for row in grp:
        data_row = []
        row_id=0
        for e in row['evals']:
            data_row.append(  (e[1], row['algorithm'], e[0],row['params']['sample_size'], e[1],row['fopt'], '%+10.9e'% ( e[1]-row['fopt']),e[2],row_id))
            row_id+=1
        data_row.sort(reverse=True)
        for r in data_row:
            coco.evalfun(*r,result=result)
    print result

