'''
Created on 18.07.2021

@author: kai
'''
import scipy.io

def LoadData(LOCALE_IDX):
    
    FILENAME_DATA="data_pkg.mat"
    FILENAME_INGREDIENTS="ingredients.mat"
    FOLDER_LOCALE=["db/de-DE/","db/de-DE-s/","db/en-US/"]
    
    matFile=scipy.io.loadmat(FOLDER_LOCALE[LOCALE_IDX]+FILENAME_DATA)
    AllIngredients=scipy.io.loadmat(FOLDER_LOCALE[LOCALE_IDX]+FILENAME_INGREDIENTS)['ingredientListUniqueType']
  
    Name=list(list(zip(*matFile['recipes']))[0])
    Name=list(list(zip(*Name))[0])
    
    Ingredients=list(list(zip(*matFile['recipes']))[1])
    for i in range(len(Ingredients)):
        Ingredients[i]=[[item.strip() for item in s] for s in Ingredients[i]]
        Ingredients[i]=[[item.replace("None","") for item in s] for s in Ingredients[i]]
    
    Link = list(list(zip(*matFile['recipes']))[2])
    Link = list(list(zip(*Link))[0])
    
    Manual=list(list(zip(*matFile['recipes']))[3])
    
    Image=list(list(zip(*matFile['recipes']))[4])
    Image=list(list(zip(*Image))[0]) 

    Container=[Name, Ingredients, Link, Manual, Image, AllIngredients]

    return Container
