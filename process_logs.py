
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




experiment = 'log:test_pop:60'

print r.llen(experiment)
data = [ast.literal_eval(i) for i in r.lrange(experiment, 0, -1)]
data.reverse()

index = 0
total = 0
for r in data:
    for e in r['evals']:
        print r['algorithm'], e[0],r['params']['sample_size'], index, e[1],r['fopt'], '%+10.9e'% ( e[1]-r['fopt']),e[2]

