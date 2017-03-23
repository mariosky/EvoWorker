
HOST="127.0.0.1"
PORT=6379
##REDISCLOUD
import urlparse, ast

import os, redis, random
import numpy as np

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

data_row = []
for r in data:
    for e in r['evals']:
        data_row.append( (r['algorithm'], e[0],r['params']['sample_size'], e[1],r['fopt'], '%+10.9e'% ( e[1]-r['fopt']),e[2]))


evalsTrigger = 1
lasteval_num = 0
fTrigger = np.inf
idxFTrigger = np.inf
nbptsf = 5
idxEvalsTrigger = 0
nbptsevals = 20
dim = 5
idxDIMEvalsTrigger = 0.
nbFirstEvalsToAlwaysWrite = 1


def evalfun( algorithm, gen, ngen, fmin, fopt, error, sol ):
    global evalsTrigger
    global lasteval_num
    global fTrigger
    global idxFTrigger
    global nbptsf
    global idxEvalsTrigger
    global nbptsevals
    global idxDIMEvalsTrigger
    global nbFirstEvalsToAlwaysWrite
    fmin = float(fmin)
    fopt = float(fopt)

    error = float(error)

    if (lasteval_num >= evalsTrigger or fmin  - fopt < fTrigger):
        #We must write if we are past the trigger?



        if lasteval_num >= evalsTrigger:
            print lasteval_num, algorithm, gen, ngen, fmin, fopt, error, sol

            while lasteval_num >= np.floor(10 ** (idxEvalsTrigger / nbptsevals)):
                idxEvalsTrigger += 1
            while lasteval_num >= dim * 10 ** idxDIMEvalsTrigger:
                idxDIMEvalsTrigger += 1
            evalsTrigger = min(np.floor(10 ** (idxEvalsTrigger / nbptsevals)),
                                    dim * 10 ** idxDIMEvalsTrigger)
            if lasteval_num < nbFirstEvalsToAlwaysWrite:
                evalsTrigger = lasteval_num + 1

        # Also if we have a better solution
        if fmin - fopt < fTrigger:  # minimization only
            print lasteval_num, algorithm, gen, ngen, fmin, fopt, error, sol,"A"
            if fmin <= fopt:
                fTrigger = -np.inf
            else:
                if np.isinf(idxFTrigger):
                   idxFTrigger = np.ceil(np.log10(fmin - fopt)) * nbptsf
                while fmin - fopt <= 10 ** (idxFTrigger / nbptsf):
                    idxFTrigger -= 1
                fTrigger = min(fTrigger, 10 ** (idxFTrigger / nbptsf))  # TODO: why?

    lasteval_num=lasteval_num+int(ngen)





for r in data_row:
    evalfun(*r)



#def evalfun( row ):
#    return row

#     """Evaluate the function, return objective function value.
#
#     Positional and keyword arguments args and kwargs are directly
#     passed to the test function evaluation method.
#
#     """
#     # This block is the opposite in Matlab!
#
#     if (self.lasteval.num + popsi >= self.evalsTrigger or
#                     np.min(ftrue) - self.fopt < self.fTrigger):  # need to write something
#
#         print self.lasteval.num, popsi, self.evalsTrigger
#         buffr = []
#         hbuffr = []
#         for j in range(0, popsi):
#             try:
#                 fvaluej = fvalue[j]
#                 ftruej = ftrue[j]
#                 xj = x[j]
#             except (IndexError, ValueError, TypeError):  # cannot slice a 0-d array
#                 fvaluej = fvalue
#                 ftruej = ftrue
#                 xj = x
#             self.lasteval.update(fvaluej, ftruej, xj)
#
#             if self.lasteval.num >= self.evalsTrigger:
#                 buffr.append(self.lasteval.sprintData(self.fopt))
#                 while self.lasteval.num >= np.floor(10 ** (self.idxEvalsTrigger / self.nbptsevals)):
#                     self.idxEvalsTrigger += 1
#                 while self.lasteval.num >= dim * 10 ** self.idxDIMEvalsTrigger:
#                     self.idxDIMEvalsTrigger += 1
#                 self.evalsTrigger = min(np.floor(10 ** (self.idxEvalsTrigger / self.nbptsevals)),
#                                         dim * 10 ** self.idxDIMEvalsTrigger)
#                 if self.lasteval.num < self.nbFirstEvalsToAlwaysWrite:
#                     self.evalsTrigger = self.lasteval.num + 1
#                 self.lasteval.is_written = True
#
#             if ftruej - self.fopt < self.fTrigger:  # minimization
#                 hbuffr.append(self.lasteval.sprintData(self.fopt))
#                 if ftruej <= self.fopt:
#                     self.fTrigger = -np.inf
#                 else:
#                     if np.isinf(self.idxFTrigger):
#                         self.idxFTrigger = np.ceil(np.log10(ftruej - self.fopt)) * self.nbptsf
#                     while ftruej - self.fopt <= 10 ** (self.idxFTrigger / self.nbptsf):
#                         self.idxFTrigger -= 1
#                     self.fTrigger = min(self.fTrigger, 10 ** (self.idxFTrigger / self.nbptsf))  # TODO: why?
#
#         # write
#         if buffr:
#             f = open(self.datafile, 'a')
#             f.writelines(buffr)
#             f.close()
#         if hbuffr:
#             f = open(self.hdatafile, 'a')
#             f.writelines(hbuffr)
#             f.close()
#     else:
#         self.lasteval.update(fvalue, ftrue, x)
#
#     return fvalue