'''
Created on 21.07.2021

@author: kai
'''
import numpy as np

def CreateShoppingCart(Ingredients):
    num=[]
    unit=[]
    name=[]
    for i in range(len(Ingredients)):
        for j in range(len(Ingredients[i])):
            num.append(Ingredients[i][j][0])
            unit.append(Ingredients[i][j][1])
            name.append(Ingredients[i][j][2])
    sortedIngredients=[num,unit,name]
    a = sortedIngredients[2]
    
    num = []
    for s in range(len(sortedIngredients[0])):
        if not sortedIngredients[0][s]:
            num.append(0)
        else:
            num.append(float(sortedIngredients[0][s]))
    
    
    unq, unq_inv, unq_cnt = np.unique(a, return_inverse=True, return_counts=True)

    accuAmount = np.zeros(len(unq))
    accuUnits = ["" for x in range(len(unq))]
    
    for i in range(len(unq_inv)):
        accuAmount[unq_inv[i]] = accuAmount[unq_inv[i]] + num[i]
        accuUnits[unq_inv[i]] = sortedIngredients[1][i]
        
    ar = []  
    for j in range(len(accuAmount)):
        ar.append([str(round(accuAmount[j],2)),str(accuUnits[j]),str(unq[j])])
    
    # sortedIngredients[2].sort()
    
    #print(ar)
    
    return ar
