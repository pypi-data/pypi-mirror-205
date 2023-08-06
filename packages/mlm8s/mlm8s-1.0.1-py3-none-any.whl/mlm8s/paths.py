import os
import random

import numpy as np
import pandas as pd

class ListedPaths:
    def __init__(self, directory=''):
        self.directory = directory
        self.list = []
        self.position = 0
        self.__gather()

    def __gather(self):

        for subdir, dirs, files in os.walk(self.directory):
            for file in files:
                self.list.append(os.path.join(subdir, file))
        self.list.sort()
        pass

    def next2(self):
        next2 = [self.list[self.position], self.list[self.position+1]]
        self.position += 1
        return next2
    
    def get_endings(self):
        endings = [path.split('.')[-1] for path in self.list]
        endings = list(dict.fromkeys(endings))        
        return endings
    
    def get_rdm(self, k=1):
        rdm_paths = random.sample(self.list, k)
        return rdm_paths

    def __len__(self):
        return len(self.list)
    
    def __add__(self, arg):
        self.list += arg.list
        self.list = list(dict.fromkeys(self.list))
        summ = ListedPaths()
        summ.list = self.list
        return summ
    
    def __mul__(self, arg):
        self.list = [path for path in self.list if path.split('.')[-1] == arg]
        prodct = ListedPaths()
        prodct.list = self.list
        return prodct
    
    def __call__(self):
        return self.list    
    
    
def strings2onehot(strings):
    df = pd.Categorical(strings, ordered=False)
    onehot = pd.get_dummies(df).to_numpy()
    return df.to_numpy(), onehot     
    
def paths2labels(paths, seperators=['/', '.'], indices=[-2, 0]):
    labels = [np.char.split(lst, sep =seperators[1])[indices[0]][indices[1]] for lst in np.char.split(paths, sep =seperators[0])]
    return labels

def paths2label_dicts(paths, seperators=['/', '.'], indices=[-2, 0]):
    labels = paths2labels(paths, seperators, indices)
    labels = list(dict.fromkeys(labels))
    keys, labels = strings2onehot(labels)
    labels_dict = dict(zip(keys, labels))
    return labels_dict

def map_via_dict(key_list, label_dict):
    return [label_dict[key] for key in key_list]
  
  
 
