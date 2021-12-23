'''
Created on 19.07.2021

@author: kai
'''
import scipy.io
from numpy import array
import random


def GetCorrelation(data,LOCALE_IDX):
    
    resultCount = 0
    
    FILENAME="cor_fac.mat"
    FOLDER_LOCALE=["db/de-DE/","db/de-DE-s/","db/en-US/"]

    annots = scipy.io.loadmat(FOLDER_LOCALE[LOCALE_IDX]+FILENAME)['CorrelationFactors']

    array_container=annots
        
    name = array(data[0][0])
    ingredients = array(data[0][1])
    link = array(data[0][2])
    instructions = array(data[0][3])
    randManNum = data[2]
    
    while resultCount < 5:
        
        if randManNum > 0:
            rand = randManNum
        else:
            rand = random.randrange(0, len(name), 1)
        seed = array_container[rand]
        index = array(seed) > data[1]
        
        i = 0
        indices = []
        while i < len(index):
            if index[i] == True:
                indices.append(i)
            i += 1
            
        result = [name[indices], array(indices), ingredients[indices], link[indices], rand, instructions[indices]]
        
        if randManNum > 0:
            resultCount = 5
        else:
            resultCount = len(result[0])
        
    data = None
        
    return result
