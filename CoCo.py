
import numpy as np

class CoCoData(object):
    def __init__(self, dim, nbptsevals= 20, nbptsf = 5):
        self.evalsTrigger = 1
        self.lasteval_num = 0
        self.fTrigger = np.inf
        self.idxFTrigger = np.inf
        self.nbptsf = nbptsf
        self.idxEvalsTrigger = 0
        self.nbptsevals = nbptsevals
        self.dim = dim
        self.idxDIMEvalsTrigger = 0.
        self.nbFirstEvalsToAlwaysWrite = 1


    def evalfun(self, algorithm, gen, ngen, fmin, fopt, error, sol, result=None ):
        fmin = float(fmin)
        fopt = float(fopt)

        error = float(error)

        if (self.lasteval_num >= self.evalsTrigger or fmin  - fopt < self.fTrigger):
            #We must write if we are past the trigger?

            if self.lasteval_num >= self.evalsTrigger:
                result.append((self.lasteval_num, algorithm, gen, ngen, fmin, fopt, error, sol))

                while self.lasteval_num >= np.floor(10 ** (self.idxEvalsTrigger / self.nbptsevals)):
                    self.idxEvalsTrigger += 1
                while self.lasteval_num >= self.dim * 10 ** self.idxDIMEvalsTrigger:
                    self.idxDIMEvalsTrigger += 1
                self.evalsTrigger = min(np.floor(10 ** (self.idxEvalsTrigger / self.nbptsevals)),
                                        self.dim * 10 ** self.idxDIMEvalsTrigger)
                if self.lasteval_num < self.nbFirstEvalsToAlwaysWrite:
                    self.evalsTrigger = self.lasteval_num + 1

            # Also if we have a better solution
            if fmin - fopt < self.fTrigger:  # minimization only
                result.append((self.lasteval_num, algorithm, gen, ngen, fmin, fopt, error, sol,'A'))
                if fmin <= fopt:
                    self.fTrigger = -np.inf
                else:
                    if np.isinf(self.idxFTrigger):
                        self.idxFTrigger = np.ceil(np.log10(fmin - fopt)) * self.nbptsf
                    while fmin - fopt <= 10 ** (self.idxFTrigger / self.nbptsf):
                        self.idxFTrigger -= 1
                    self.fTrigger = min(self.fTrigger, 10 ** (self.idxFTrigger / self.nbptsf))  # TODO: why?

        self.lasteval_num=self.lasteval_num+int(ngen)