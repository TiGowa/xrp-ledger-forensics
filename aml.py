import urllib.request, requests, json, io, sys
from urllib.request import Request, urlopen

"""Get list of fraudulent wallets."""

ref = Request('https://xrpforensics.org/api/advisory/advisory.json', headers={'User-Agent': 'Chrome/78.0.3904.97'})
webpage = urlopen(ref).read()
dic = json.loads(webpage)
lis = list(dic)

wallet = input ("Enter your wallet address:")

"""Look if wallet given in input is identified as fraudulent"""

for address in dic:
    if address == wallet:
        print ("Your address is identified as fraudulent: *Go to hell!*")
        sys.exit()

"""Credit to: https://hackersandslackers.com/extract-data-from-complex-json-python/"""

def extract_values(obj, key):

    """Pull all values of specified key from nested JSON."""

    arr = []

    def extract(obj, arr, key):

        """Recursively search for values of key in JSON tree."""

        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    results = extract(obj, arr, key)
    return results

"""Get index of duplicated string in a list | Credit https://www.quora.com/How-do-I-get-the-index-of-a-duplicated-string-in-a-list-Python-2"""

def getAllindex(list, value):
     return filter(lambda a: list[a]==value, range(0,len(list)))

"""Scan more transactions if wallet in input has more than 1000 tx"""

def query(q):
    dic = json.loads(webpage)
    PARAMS = {"result": "tesSUCCESS", "limit": "1000", "marker": q}
    req = requests.get ('http://data.ripple.com/v2/accounts/{}/transactions'.format(wallet), params=PARAMS).json()
    
    for h in req['transactions']:
        k = extract_values(h, 'Account')
        gethash = h['hash']
        lis = list(dic)
        for i in k:
            for ii in lis:
                if i == ii:
                    print("You have been involved with this address: ",ii," identified as fraudulent by https://xrpforensics.org/list/")
                    print("here is the hash of the tx: ",gethash)
                    lis.remove(ii)
                    
    if "marker" in req.keys():
        nextpage = req['marker']
        query(nextpage)

q = ""
PARAMS = {"result": "tesSUCCESS", "limit": "1000", "marker": q}
req = requests.get ('http://data.ripple.com/v2/accounts/{}/transactions'.format(wallet), params=PARAMS).json()

for h in req['transactions']:
    k = extract_values(h, 'Account')
    gethash = h['hash']
    lis = list(dic)
    for i in k:
        for ii in lis:
            if i == ii:
                print("You have been involved with this address: ",ii," identified as fraudulent by https://xrpforensics.org/list/")
                print("here is the hash of the tx: ",gethash)
                lis.remove(ii)

if "marker" in req.keys():
    nextpage = req['marker']
    query(nextpage)


