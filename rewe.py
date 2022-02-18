'''
Created on 30.06.2021

@author: kai
'''
from ReweMobileApi import ReweMobileApi

from numpy import array, ones, zeros
from _ast import Try
import re


def searchReweItem(shoppingCart):
    global rewe
    
    failedItems = []
    items = []
    reqItem = []
    
    for i in range(len(shoppingCart)):
        searchresults = rewe.searchItem(shoppingCart[i][2])
        
        if searchresults=="error,429":
            return(searchresults)
        
        try:
            if not searchresults:
                failedItems.append(shoppingCart[i][0] + " " + shoppingCart[i][1] + " " + shoppingCart[i][2] )
            else:
                items.append(searchresults)
                reqItem.append(shoppingCart[i])
        except:
            print("Error in rewe search - item: " + str(i))
            
        
    return [items,failedItems,reqItem]

def setReweItem(items):
    global rewe
    
    name = []
    price = []
    amount = []
    id = []
    failedItems = []
    quantityTooLow = ones(len(items[0]), dtype=bool)
    
    for i in range(len(items[0])):
        name.append(items[0][i][0]['productName'] + " (" + items[2][i][2] + ")")

        try:
            price.append(items[0][i][0]['_embedded']['articles'][0]['_embedded']['listing']['pricing']['currentRetailPrice']/100)
        except:
            print("no price found - item:" + str(i))
            
            
        amount.append(items[0][i][0]['_embedded']['articles'][0]['_embedded']['listing']['pricing']['grammage']+ " (" + items[2][i][0] + " " + items[2][i][1] + ")")
        id.append(items[0][i][0]['_embedded']['articles'][0]['_embedded']['listing']['id'])
        picnicQnt = re.sub("([0-9]*[.]?[0-9]*[.]?).*","\g<1>",items[0][i][0]['_embedded']['articles'][0]['_embedded']['listing']['pricing']['grammage'])
        if not picnicQnt:
            pass
        else:
            if float(picnicQnt) >= float(items[2][i][0]):
                quantityTooLow[i] = False
            else:
                quantityTooLow[i] = True
    
    ar = []  
    sumCosts = 0
    for j in range(len(name)):
        #ar.append([str(accuAmount[j]),str(accuUnits[j]),str(unq[j])])
        ar.append([str(name[j]),str(price[j]),str(amount[j]),str(id[j])])
        sumCosts = sumCosts + price[j]
        #str(failedItems)
        
    return [ar,failedItems,str(round(sumCosts,2)),id,quantityTooLow]
    

def changeItem():
    print()

def rewePutOrder(items):
    global rewe
    
    for i in range(len(items)):
        #picnic.add_product(items[i][3], count=1)
        rewe.addItem2Basket(items[i][3],1)
        
    
    print("OK")
    
def reweDoLogin(userdata):
    global rewe
    authStatus = False
    
    try:
        rewe = ReweMobileApi()
        authStatus = rewe.login(userdata[0],userdata[1],userdata[2])
    except:
        authStatus = False
        
    
    return authStatus