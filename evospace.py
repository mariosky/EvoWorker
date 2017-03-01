import requests


class EvoSpace(object):
    def __init__(self, server, space):
        self.server = server
        self.space = space
        self.url = 'http://%s/%s/'%(self.server,self.space)

    def get(self,size):
        r = requests.get(self.url+'' )
        print r.text
        return r

