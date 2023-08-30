import json
from web3 import Web3
from utils import *

# eth = 'https://eth.llamarpc.com'
bsc = 'https://bsc-dataseed.binance.org/'
web3 = Web3(Web3.HTTPProvider(bsc))

# #log if we're connected or not
print('web3.is_connected =>',web3.is_connected())



with open('private_key.json', 'r') as fp:
    _key_obj = json.load(fp)["_key_obj"]
wallet = web3.eth.account.from_key(_key_obj)
print('_address=>',wallet._address)
balance = web3.eth.get_balance(wallet._address)
balance  = web3.from_wei(balance,'ether')
print('BNB balance =>',balance) 


dest_account = "0x744Df4223330321C57e1EeE168E26395913C6eB2"


nonce = web3.eth.get_transaction_count(wallet._address)

#build the transaction
#build a dictionary that contains all the transaction information
tx = {
'nonce': nonce,  #prevents from sending a transaction twice on ethereum
'to': dest_account,
'value': web3.to_wei(0.05, 'ether'),
'gas': 250000,
'gasPrice': web3.eth.gas_price
}

#sign the transaction
signed_tx = web3.eth.account.sign_transaction(tx, wallet._private_key)
#send the transaction
tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)

#get transaction hash
print(web3.to_hex(tx_hash)) #to convert the hash into hexadecimal
