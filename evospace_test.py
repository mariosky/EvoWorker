import requests
import json
import random


#Delete  population
r = requests.delete('http://127.0.0.1:3000/evospace/test_pop')
print "Delete population"


#Initialize population
r = requests.post('http://127.0.0.1:3000/evospace/test_pop/initialize')
print "Create population", r.text


#Add Individuals
ind = {'id':'id:3:2', 'name':"Mario", 'chromosome':[1,2,3,1,1,2,2,2],"fitness":{"s":1},"score":random.randint(1,1000) }
url = 'http://127.0.0.1:3000/evospace/test_pop/individual'
r = requests.post(url, data=ind)
print "Insert individual with id", r.text

# Add 10 Individuals
print "Insert 10 individuals", r.text
for i in range(10):
	ind = { 'name':"Mario", 'chromosome':[2,2,3,1,1,2,2,2],"fitness":{"s":i},"score":random.randint(1,1000)}
	url = 'http://127.0.0.1:3000/evospace/test_pop/individual'
	r = requests.post(url, data=ind)
print "Insert individual with out id", r.text

#Read an individual by id
url = 'http://127.0.0.1:3000/evospace/test_pop/individual/3'
r = requests.get(url)
print "Read an individual by key", r.json()['id'], r.json()['chromosome']

# Read All the population keys
url = 'http://127.0.0.1:3000/evospace/test_pop'
print "\n\nAll the population keys:"
r = requests.get(url)
for i in r.json():
    print i

# Read All the population
url = 'http://127.0.0.1:3000/evospace/test_pop/all'
r = requests.get(url)
print "\n\nRead all"
for i in r.json()['population']['sample']:
    print i

#Read those individuals with a score between [:start] and [:finish].
url = 'http://127.0.0.1:3000/evospace/test_pop/zrange/1/1'
r = requests.get(url)
print "\nscore between 10 and 12:", r.text

#Read the top N individuals
url = 'http://127.0.0.1:3000/evospace/test_pop/top/2'
r = requests.get(url)
top = r.json()
print "\n\ntopn"
print top,type(top['sample'])
for i in top['sample']:
    print i['score']

#GET sample of N individuals
url = 'http://127.0.0.1:3000/evospace/test_pop/sample/2'
r = requests.get(url)
print "\n Get sample (3):"
sample = r.json()
for i in sample['result']['sample']:
    print i['id']

#GET sample of N individuals
url = 'http://127.0.0.1:3000/evospace/test_pop/sample/3'
r = requests.get(url)
print "\n Get sample (3):"
sample = r.json()
for i in sample['result']['sample']:
    print i['id']

# Read All the population keys
url = 'http://127.0.0.1:3000/evospace/test_pop'
print "\n\nAll the population keys:"
r = requests.get(url)
for i in r.json():
   print i

# Read those individuals with a score between [:start] and [:finish].
url = 'http://127.0.0.1:3000/evospace/test_pop/sample_queue'
r = requests.get(url)
print "\nsample queue:", r.text




#PUT BACK a sample
ind ={'sample':sample['result']['sample'], 'sample_id':sample['result']['sample_id']}
print "sample:",ind,json.dumps(ind)
url = 'http://127.0.0.1:3000/evospace/test_pop/sample'
r = requests.put(url, json=ind)
print '\n\n PUT back sample', r.text

# Read All the population keys
url = 'http://127.0.0.1:3000/evospace/test_pop'
print "\n\nAll the population keys:"
r = requests.get(url)
for i in r.json():
   print i


#POST sample  INSERT
ind ={'sample': [{ 'name':"Mario", 'chromosome':[2,2,3,1,1,2,2,2],"fitness":{"s":i},"score":random.randint(1,1000) }  for i in range(20, 30)] }
url = 'http://127.0.0.1:3000/evospace/test_pop/sample'
r = requests.post(url, json=ind)
print '\n\nPOST sample', r.text

# Read All the population keys
url = 'http://127.0.0.1:3000/evospace/test_pop'
print "\n\nAll the population keys:"
r = requests.get(url)
for i in r.json():
   print i


#Read the number of individuals in the population [space]
url = 'http://127.0.0.1:3000/evospace/test_pop/cardinality'
r = requests.get(url)
print "\ncardinality", r.text

#Respawn 1 sample
url = 'http://127.0.0.1:3000/evospace/test_pop/respawn'
data ={'n':1}
r = requests.post(url,data)
print "\nrespawn", r.text

# Read All the population keys
url = 'http://127.0.0.1:3000/evospace/test_pop'
print "\n\nAll the population keys:"
r = requests.get(url)
for i in r.json():
   print i

#Read the number of individuals in the population [space]
url = 'http://127.0.0.1:3000/evospace/test_pop/cardinality'
r = requests.get(url)
print "\ncardinality", r.text

r.connection.close()
