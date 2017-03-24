
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


EXPERIMENT_ID = 106
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


grp_benchmark = itemgetter("benchmark","dim")
grp_instance = itemgetter("benchmark","instance")
result = []
new_info = True
for key, benchmark_group in groupby(data, grp_benchmark):
    #Create folder if not exisits
    folder = DATA_FOLDER + '/F' + str(key[0])
    try:
        os.makedirs(folder)
    except OSError:
        pass

    indexfile = DATA_FOLDER + '%s.info' % ( '/F' + str(key[0]))

    # Create files
    filename = '%s-%02d_f%s_DIM%d' % (str(EXPERIMENT_ID), 0,
                                      str(key[0]), key[1])
    datafile =  folder+'/' + filename + '.tdat'
    hdatafile = folder+'/' + filename + '.dat'

    print "F" + str(key[0]) + " Dimension:" + str(key[1])

    comment = "% EvoSpace: Pool Based Algorithm see info in root folder"
    if new_info:
        info = """funcId = %s, DIM = %d, Precision = 1.000e-08, algId = 'EvoSpace'\n%s\nF%s/%s.dat, """ % \
           (str(key[0]), key[1], comment, key[0],filename)
        new_info = False
    else:
        info = """\nfuncId = %s, DIM = %d, Precision = 1.000e-08, algId = 'EvoSpace'\n%s\nF%s/%s.dat, """ % \
               (str(key[0]), key[1], comment, key[0], filename)


    f = open(indexfile, 'a')
    f.writelines(info)

    f.close()
    new_instance = True

    for key,benchmark in groupby(benchmark_group, grp_instance):
        print  " Instance:" + str(key[1])


        coco = CoCoData(5)
        index = 0
        total = 0
        buffr = []
        hbuffr =[]

        for row in benchmark:
            data_row = []
            row_id=0
            for e in row['evals']:
                data_row.append((e[1], row['algorithm'], e[0],row['params']['sample_size'], e[1],row['fopt'], '%+10.9e'% ( e[1]-row['fopt']),e[2]))
                row_id+=1
            data_row.sort(reverse=True)
            for r in data_row:
                coco.evalfun(*r[1:],buffr=buffr,hbuffr=hbuffr)

        if buffr:
            f = open(datafile, 'a')
            f.write('%% function evaluation | noise-free fitness - Fopt'
                    ' () | best noise-free fitness - Fopt | measured '
                    'fitness | best measured fitness | x1 | x2...\n'
                    )

            f.writelines(buffr)

            f.close()
        if hbuffr:
            f = open(hdatafile, 'a')
            f.write('%% function evaluation | noise-free fitness - Fopt'
                    ' () | best noise-free fitness - Fopt | measured '
                    'fitness | best measured fitness | x1 | x2...\n'
                    )
            f.writelines(hbuffr)
            f.close()
        last = hbuffr[-1].split(" ")




        f = open(indexfile, 'a')
        if new_instance:
            f.write('%s:%d|%.1e' % (key[1],int(last[0]), float(last[1])))
            new_instance = False
        else:
            f.write(', %s:%d|%.1e' % (key[1], int(last[0]), float(last[1])))

        f.close()




