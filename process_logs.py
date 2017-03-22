
HOST="127.0.0.1"
PORT=6379
##REDISCLOUD
import urlparse, ast

import os, redis, random

if os.environ.get('REDISTOGO_URL'):
    url = urlparse.urlparse(os.environ.get('REDISTOGO_URL'))
    r = redis.Redis(host=url.hostname, port=url.port, password=url.password)
#LOCAL
else:
    r = redis.Redis(host=HOST, port=PORT)




experiment = 'log:test_pop:50'

print r.llen(experiment)
data = [ast.literal_eval(i) for i in r.lrange(experiment, 0, -1)]

index = 0
total = 0
for r in data:
    print r
    for e in r['evals']:
        print r['algorithm'], total, index, e[1],r['fopt'], '%+10.9e'% ( e[1]-r['fopt'])
        index+=1
        total+=r['params']['sample_size']