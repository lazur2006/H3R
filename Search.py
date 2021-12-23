'''
Created on 22.07.2021

@author: kai
'''
from numpy import array
  
def SearchRecipes(ret):
    
    name = []
    indices = []
    ingredients = []
    link = []
    instructions = []
     
    for i in range(len(ret[0])):
        for j in range(len(ret[1][0])):
            
            Ingredients = ret[1][1][j]
            num_ = []
            unit_ = []
            name_ = []
            for k in range(len(Ingredients)):
                num_.append(Ingredients[k][0])
                unit_.append(Ingredients[k][1])
                name_.append(Ingredients[k][2])
            sortedIngredients = [num_, unit_, name_]
            a = sortedIngredients[2]
            
            if ret[0][i].strip() in a:
                name.append(ret[1][0][j])
                indices.append(j)
                ingredients.append(ret[1][1][j])
                link.append(ret[1][2][j])
                instructions.append(ret[1][3][j])
        
    result =    [array(name), array(indices), array(ingredients), array(link), '', array(instructions)]
    
    return result
    
