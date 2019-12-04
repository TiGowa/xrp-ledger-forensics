import urllib.request, requests, json, io, sys

from urllib.request import Request, urlopen

req = Request('https://xrpforensics.org/api/advisory/advisory.json', headers={'User-Agent': 'Chrome/78.0.3904.97'})
webpage = urlopen(req).read()
dic1 = json.loads(webpage)

wallet = input ("Enter your wallet address:")

for address in dic1:
    if address == wallet:
        print ("Your address is identified as fraudulent: *Go to hell!*")
        sys.exit()

PARAMS = {"result": "tesSUCCESS", "descending": "true", "limit": "1000"}

req = requests.get ('http://data.ripple.com/v2/accounts/{}/transactions'.format(wallet), params=PARAMS).json()

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

account = extract_values(req, 'Account')

for i in account:
    for ii in list(dic1):
        if i == ii:
            print("OOops! You have been involved with this address ",ii," identified as fraudulent by https://xrpforensics.org/list/")
            dic1.pop(ii)
