import requests
import urllib.parse
import webbrowser
import re

def put_order(ingredients):
    #imageLink = "https://i.ibb.co/nR1W24x/Hello-N00b.jpg"
    imageLink = ""
    #ingredients = ["1 Einheit Tomate","2 Stück Gurke"]
    
    str = "["
    for i in range(len(ingredients)):
        str += '"' + re.sub('\„|\“|\"',"",ingredients[i]) + '"'
        if i<len(ingredients)-1:  # print a separator if this isn't the first element
            str += ","
    str += "]"
    
    query = """{"@context":"http://schema.org/",
    "@type":"Recipe","@id":"https://www.n00b.no",
    "name":"HelloFresh3R",
    "image":[""," """+imageLink+""";*,*"],
    "author":{"@type":"Person","name":""},
    "description":"",
    "keywords":"",
    "aggregateRating":{"@type":"AggregateRating","ratingValue":10,"reviewCount":17},
    "totalTime":"PT30M",
    "recipeYield":"2 persons",
    "nutrition":{"@type":"NutritionInformation","servingSize":"2 persons","calories":"666 kcal"},
    "recipeIngredient":"""+str+""",
    "recipeInstructions":"","overrides":null}"""
    
    
    
    enc_query = urllib.parse.quote(query)
    
    session = requests.Session()
    
    url = "https://shop.rewe.de/api/recipes/mapping/?partnerDomain=rewe.de"
    
    payload='data='+enc_query
    headers = {
      'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
      'sec-ch-ua-mobile': '?0',
      'Upgrade-Insecure-Requests': '1',
      'Content-Type': 'application/x-www-form-urlencoded',
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    }
    
    response = session.request("POST", url, headers=headers, data=payload)
    
    print(response.url)
    
    webbrowser.open(response.url, new=2)