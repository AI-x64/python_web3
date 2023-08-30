import json
from web3 import Web3
from utils import *

# eth = 'https://eth.llamarpc.com'
bsc = 'https://bsc-dataseed.binance.org/'
web3 = Web3(Web3.HTTPProvider(bsc))

# #log if we're connected or not
print('web3.is_connected =>',web3.is_connected())



############################################
############################################
routerPCS = '0x10ED43C718714eb63d5aA57B78B54704E256024E'
BUSD = '0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56'
WBNB = '0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c'
CAKE = '0x0E09FaBB73Bd3Ade0a17ECC321fD13a19e81cE82'
############################################
############################################




with open('private_key.json', 'r') as fp:
    _key_obj = json.load(fp)["_key_obj"]
wallet = web3.eth.account.from_key(_key_obj)
print('_address=>',wallet._address)
balance = web3.eth.get_balance(wallet._address)
balance  = web3.from_wei(balance,'ether')
print('BNB balance =>',balance) 



routerContract = get_router_contract(routerPCS,web3)

_amnt = 1
print(str(_amnt)+' WBNB=>BUSD',calc_token_price(_amnt,WBNB,BUSD,routerContract,web3))

_amnt = 1
print(str(_amnt)+' CAKE=>BUSD',calc_token_price(_amnt,CAKE,BUSD,routerContract,web3))

_amnt = 0.05
print(str(_amnt)+' WBNB=>CAKE',calc_token_price(_amnt,WBNB,CAKE,routerContract,web3))


