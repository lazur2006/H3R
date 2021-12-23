'''
Created on 21.07.2021

@author: kai
'''
import re
#from IngredientConstraints import setIngredientConstraints

def filterIngredients(Ingredients):
    
    concatAmount = []
    concatUnit = []
    concatIngredients = []
    
    #regPattern = ".*Stück |.*\d g |.*Esslöffel |.*Einheit |.*Geschmack |.*ml |.*Dose |.*Teelöffel | '|[*]|.*Packung |.*mg |.*Zweig |\d*[.]?\d |/ für \d Personen / für \d Personen(?=.*)"
    regPattern = "(\d*[.]?\d*)?\s?(Stück|g|Esslöffel|Einheit|Geschmack|ml|Dose|Teelöffel|Packung|mg|nach Geschmack|Zweig|/ für \d Personen / für \d Personen)?\s?([^*]*)"
    half = "½"
    quarter = "¼"
    threeQuarter = "¾"
    threeFifth = "⅗"

    endStringWhitespaces = "\s*$"
    
    AllIngredients = []
        
    for j in range(len(Ingredients)):
        for k in range(len(Ingredients[j])):
            regex = re.match(regPattern, re.sub(half, '0.5', re.sub(quarter, '0.25', re.sub(threeQuarter, '0.75', re.sub(threeFifth, '0.6', re.sub(endStringWhitespaces, '', Ingredients[j][k]))))))
            concatAmount.append(regex.group(1))
            concatUnit.append(regex.group(2))
            concatIngredients.append(regex.group(3))
            # ret = ret.capitalize()
            #
            AllIngredients.append(re.sub(half, '0.5', re.sub(quarter, '0.25', re.sub(endStringWhitespaces, '', Ingredients[j][k]))))
            
    #concatIngredients = setIngredientConstraints(concatIngredients)
            
    return [concatAmount,concatUnit,concatIngredients]
