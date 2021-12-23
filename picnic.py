'''
Created on 30.06.2021

@author: kai
'''
from python_picnic_api import PicnicAPI
#from symbol import except_clause
from numpy import array, ones, zeros
from _ast import Try
import re


def searchPicnicItem(shoppingCart):
    global picnic
    
    failedItems = []
    items = []
    reqItem = []
    
    for i in range(len(shoppingCart)):
        searchresults = picnic.search(shoppingCart[i][2])
        try:
            error = searchresults['error']['code'] == "BAD_REQUEST"
        except:
            error = False   
           
        if error:
            pass
        else:
            if not searchresults[0]['items']:
                failedItems.append(shoppingCart[i][0] + " " + shoppingCart[i][1] + " " + shoppingCart[i][2] )
            else:
                items.append(searchresults[0]['items'])
                reqItem.append(shoppingCart[i])
        
    return [items,failedItems,reqItem]

def setPicnicItem(items):
    global picnic
    
    name = []
    price = []
    amount = []
    id = []
    failedItems = []
    quantityTooLow = ones(len(items[0]), dtype=bool)
    
    for i in range(len(items[0])):
        name.append(items[0][i][0]['name'] + " (" + items[2][i][2] + ")")

        try:
            price.append(items[0][i][0]['price']/100)
        except:
            price.append(items[0][i][0]['display_price']/100)
            
            
        amount.append(items[0][i][0]['unit_quantity']+ " (" + items[2][i][0] + " " + items[2][i][1] + ")")
        id.append(items[0][i][0]['id'])
        picnicQnt = re.sub("[^0-9][.]?(\d*[.]?\d?)","\g<1>",items[0][i][0]['unit_quantity'])
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
        ar.append([str(name[j]),str(price[j])+" €",str(amount[j]),str(id[j])])
        sumCosts = sumCosts + price[j]
        #str(failedItems)
        
    return [ar,failedItems,str(round(sumCosts,2)),id,quantityTooLow]
    

def changeItem():
    print()

def putOrder(items):
    global picnic
    
    for i in range(len(items)):
        picnic.add_product(items[i][3], count=1)
        
    
    print("OK")
    
def doLogin(userdata):
    global picnic
    authStatus = False
    
    try:
        picnic = PicnicAPI(username=userdata[0],password=userdata[1],country_code='DE')
        authStatus = picnic.session.authenticated
    except:
        authStatus = False
        
    
    return authStatus

