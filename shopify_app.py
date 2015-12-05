import shopify
import csv
import json
import os
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

def checkIfPresent(collections,item):
    for collection in collections:
        if collection == item:
            return True
    return False

API_KEY = 'f4d656257f2542f2d3a0f3b8cf4a6b65'
PASSWORD = '37e6b3faa10b8a3bb504cb925184b878'
SHARED_SECRET = '6d697bf07889c8ac0e89e64dc993a5de'
shop_url = "https://%s:%s@botre.myshopify.com/admin" % (API_KEY, PASSWORD)
shopify.ShopifyResource.set_site(shop_url)
shopify.Session.setup(api_key=API_KEY, secret=SHARED_SECRET)
shop = shopify.Shop.current()

collections_json = {}
collections = []
try:
         json_file_path =  os.path.join(__location__, 'collections.json')
         with open(json_file_path) as data_file:
            collections_json = json.load(data_file)
         if 'collections' in collections_json:
             collections = collections_json['collections']
         else:
             collections = []
         file_path =  os.path.join(__location__, 'input.csv')
         with open(file_path) as csvfile:
            total = len(list(csv.reader(open(file_path))))
            reader = csv.DictReader(csvfile)
            count = 0
            for row in reader:
               count = count + 1
               if 'name' in row and 'picture url' in row and 'title contains condition' in row:
                   if row['name'] != '' and checkIfPresent(collections,row['name'])==False :
                       print 'Progress : ' + str(int(float(count)/total * 100)) + '%'
                       sm = shopify.SmartCollection({
                           "title": row['name'],
                           "image": {
                             "src": row['picture url']
                           },
                           "rules": [
                             {
                               "column": "title",
                               "relation": "contains",
                               "condition": row['title contains condition']
                             }
                           ]
                       })
                       try :
                           if sm.save():
                               collections.append(row['name'])
                               collections_json['collections'] = collections
                               with open(json_file_path, 'w') as outfile:
                                      json.dump(collections_json, outfile)
                               print row['name'] + ' saved '
                           elif sm.errors:
                               print row['name'] + ' was not saved '
                               print sm.errors.full_messages()
                       except Exception as e:
                           print e




except Exception as e:
    print e

print 'SmartCollection Upload Complete'
