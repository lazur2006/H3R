'''
Created on 18.01.2022

@author: lazur2006
'''
'''
import requests module
'''
import requests
'''
import ssl and adapters
'''
import ssl
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
from requests.packages.urllib3.util import ssl_
'''
setup cipher suite
'''
ciphers = (
'''ECDHE-ECDSA-AES128-GCM-SHA256:'''
'''ECDHE-RSA-AES128-GCM-SHA256:'''
'''ECDHE-ECDSA-AES256-GCM-SHA384:'''
'''ECDHE-RSA-AES256-GCM-SHA384:'''
'''ECDHE-ECDSA-CHACHA20-POLY1305:'''
'''ECDHE-RSA-CHACHA20-POLY1305:'''
'''DHE-RSA-AES128-GCM-SHA256:'''
'''DHE-RSA-AES256-GCM-SHA384'''
)
'''
import pickle module for handling cookie data stream
'''
import pickle
'''
setup REWE header
'''
useragent = 'REWE-Mobile-App/3.4.50 Android/7.0 (Smartphone)'

base = "https://mobile-api.rewe.de/mobile"

'''
import other stuff
'''
import json
import time
from random import randint

class TlsAdapter(HTTPAdapter):

    def __init__(self, ssl_options=0, **kwargs):
        self.ssl_options = ssl_options
        super(TlsAdapter, self).__init__(**kwargs)

    def init_poolmanager(self, *pool_args, **pool_kwargs):
        ctx = ssl_.create_urllib3_context(ciphers=ciphers, 
                                          cert_reqs=ssl.CERT_REQUIRED, 
                                          options=self.ssl_options)
        self.poolmanager = PoolManager(*pool_args,
                                       ssl_context=ctx,
                                       **pool_kwargs)
        
class ReweMobileApi():
    
    def __init__(self):
        super(ReweMobileApi, self).__init__()
        # Mount session due to cloudflare's TLS fingerprint protection
        self.session = requests.session()
        self.adapter = TlsAdapter(ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1)
        self.session.mount("https://", self.adapter)
        
        self.refreshToken = ""
        
        
        '''Get latest cookies and refreh token'''
        self.init_cookies_token()
        
    def init_cookies_token(self):
        '''returns true if cookies available and valid'''
        try:
            with open('_cookies', 'rb') as f:
                self.session.cookies.update(pickle.load(f))
            with open('_token', 'rb') as f:
                self.refreshToken = pickle.load(f)
            with open('_misc', 'rb') as f:
                self.rJson = pickle.load(f)
                self.rd_market_id = self.rJson['customer']['market']['wwIdent']
            return(True)
        except:
            return(False)
        
    def getDeviceAuthToken(self,IpAddress):
        url = f"http://{IpAddress}:8080/deviceAuthToken"
        try:
            r = self.session.request("GET", url,timeout=1).json()['deviceAuthToken']
            if r=="init":
                print("(advice) >>> Press app authenticate button")
                return(None)
            else:
                return(r)
        except:
            print("(advice) >>> Auth app is offline")
            return(None)
            
    def login(self,user,password,AndroidDeviceIp):
        
        if self.refreshBearer():
            self.getBasket()
            return(True)
        else:        
            url = f"{base}/customer/login"
    
            payload = json.dumps({
              "username": user,
              "password": password,
              "recaptchaToken": self.getDeviceAuthToken(AndroidDeviceIp)
            })
    
            headers = {
              'user-agent': useragent,
              'content-type': 'application/json; charset=UTF-8',
            }
            
            r = self.session.request("POST", url, headers=headers, data=payload)
            
            if r.status_code == 429:
                print("(error) >>> Too many requests")
                print(f"Retry after {r.headers['Retry-After']} seconds")
            if r.status_code != 200:
                print("(error) >>> Login refused by server")
                return(False)
            
            self.rd_market_id = r.json()['customer']['market']['wwIdent']
            
            self.save_cookies_token(r)
            
            self.getBasket()
            
            return(True)
        
    def refreshBearer(self):        
        url = f"{base}/customer/refresh"
        payload = json.dumps({
          "refreshToken": self.refreshToken
        })
        headers = {
          'host': 'mobile-api.rewe.de',
          'content-type': 'application/json',
          'user-agent': useragent
        }
        r = self.session.request("POST", url, headers=headers, data=payload)
        if r.status_code != 200:
            print("(advice) >>> Refresh auth failed. Start login attemp")
            return(False)
        else:
            print("(advice) >>> Early login successfull")
            self.save_cookies_token(r)
            return(True)
        
    def save_cookies_token(self,r):
        self.bearer = r.json()['token']['access_token']
        self.refreshToken = r.json()['token']['refresh_token']
        
        with open('_cookies', 'wb') as file:
            pickle.dump(self.session.cookies, 
                        file, 
                        protocol=pickle.HIGHEST_PROTOCOL)
        with open('_token', 'wb') as file:
            pickle.dump(self.refreshToken, 
                        file, 
                        protocol=pickle.HIGHEST_PROTOCOL)
        with open('_misc', 'wb') as file:
            pickle.dump(r.json(), 
                        file, 
                        protocol=pickle.HIGHEST_PROTOCOL)
        
    def getUser(self):
        url = f"{base}/customer/profile"

        headers = {
          'host': 'mobile-api.rewe.de',
          'authorization': f"Bearer {self.bearer}",
          'user-agent': useragent,
          'content-type': 'application/json'
        }
        
        return(self.session.request("GET", url, headers=headers).json())
    
    def getBasket(self):
        url = f"{base}/basket"
        headers = {
          'host': 'mobile-api.rewe.de',
          'authorization': f"Bearer {self.bearer}",
          'user-agent': useragent,
          'rd-service-types': 'DELIVERY'
        }
        r = self.session.request("GET", url, headers=headers).json()
        
        '''When basket is empty there is no merchantBaskets -> storeId object'''
        #self.rd_market_id = r['merchantBaskets'][0]['storeId']
        self.basketId = r['id']
        self.basketVersion = r['version']
        return(r)
    
    def searchItem(self,query):
        url = f"https://shop.rewe.de/api/products?search={query}&market={self.rd_market_id}"
        
        headers = {
            'User-Agent': useragent,
            'content-type': 'application/json',
            'x-device-accept': 'application/vnd.com.rewe.digital.basket-ui+json',
        }
        
        r = requests.request("GET", url, headers=headers)
        
        if r.status_code == 429:
                print("(error) >>> Too many requests")
                print(f"Retry after {r.headers['Retry-After']} seconds")
                print("")
                return("error,429")
        return(r.json()['_embedded']['products'])
    
    def addItem2Basket(self,productObj,quantity):
        url = f"{base}/basket/{self.basketId}"

        payload = json.dumps({
          "version": self.basketVersion,
          "actions": [
            {
              "lineItem": {
                "quantity": quantity,
                "listing": {
                  #"version": productObj['rawValues']['listingVersion'],
                  "id": productObj#['rawValues']['listingId']
                }
              },
              "action": "modifyLineItem",
              "merchantName": "REWE"
            }
          ]
        })
        headers = {
          'User-Agent': useragent,
          'Authorization': f"Bearer {self.bearer}",
          'rd-basket-id': self.basketId,
          'Content-Type': 'application/json',
        }
        
        r = self.session.request("PATCH", url, headers=headers, data=payload)
        
        if r.status_code == 429:
                print("(error) >>> Too many requests")
                print(f"Retry after {r.headers['Retry-After']} seconds")
                print("")
                
        self.basketVersion = r.json()['version']

# if __name__ == '__main__':
#     api = REWEapi()
#     auth = api.login('xxxxx@xxxxx.com','11111111',"192.168.0.xxx")
#     basket = api.getBasket()
#     search_results = api.searchItem("cola")
#
#     '''Adds first 5 cola products for two times to basket'''
#     for i in range(5):
#         api.addItem2Basket(search_results[i],0)
#
#     print("(advice) >>> script finshed")
#     pass
    