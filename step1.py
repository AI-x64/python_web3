import json
from web3 import Web3

# eth = 'https://eth.llamarpc.com'
bsc = 'https://bsc-dataseed.binance.org/'
web3 = Web3(Web3.HTTPProvider(bsc))

# #log if we're connected or not
print('web3.is_connected =>',web3.is_connected())

try:
    with open('private_key.json', 'r') as fp:
        _key_obj = json.load(fp)["_key_obj"]
    wallet = web3.eth.account.from_key(_key_obj)
    print(wallet._address)
    print(wallet._private_key)
    print(wallet._key_obj)
    balance = web3.eth.get_balance(wallet._address)
    balance  = web3.from_wei(balance,'ether')
    print('BNB balance =>',balance)    
except:
    wallet = web3.eth.account.create()
    print(wallet._address)
    print(wallet._private_key)
    print(wallet._key_obj)
    balance = web3.eth.get_balance(wallet._address)
    balance  = web3.from_wei(balance,'ether')
    print('BNB balance =>',balance)
    _key_obj = {}
    _key_obj["_key_obj"] = str(wallet._key_obj)
    with open('private_key.json', 'w') as fp:
         json.dump(_key_obj, fp, indent=4)
