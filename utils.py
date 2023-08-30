import json
import requests
import time

############################################################
############################################################
def get_abi(_address,web3):
    abi_address = web3.to_checksum_address(_address)
    url_eth = 'https://api.bscscan.com/api'
    API_ENDPOINT = url_eth + '?module=contract&action=getabi&address=' + str(abi_address)
    r = requests.get(url = API_ENDPOINT)
    response = r.json()
    _abi = json.loads(response['result'])
    return _abi  
############################################################
############################################################
def get_router_contract(_address,web3):
    _abi = get_abi(_address,web3)
    router_contract = web3.eth.contract(address=_address, abi=_abi)
    return router_contract

############################################################
############################################################
def calc_token_price(amount,token_address1,token_address2,router_contract,web3):
    oneToken = web3.to_wei(amount, 'ether')
    price = router_contract.functions.getAmountsOut(oneToken, [token_address1, token_address2]).call()
    normalizedPrice = web3.from_wei(price[1], 'ether')
    return round(normalizedPrice,3)

############################################################
############################################################
def get_token_name_and_symbol(token_address,web3):
    token_abi = get_abi(token_address,web3)
    token_contract = web3.eth.contract(address=token_address, abi=token_abi)
    token_name = token_contract.functions.name().call()
    token_symbol = token_contract.functions.symbol().call()
    return token_name,token_symbol



############################################################
############################################################
def buy_token_using_eth(wallet,buy_amount,toke_to_buy,spend,router_contract,web3):
    address = wallet._address
    nonce = web3.eth.get_transaction_count(address)
    gas_price = web3.eth.gas_price

    SWP_txn = router_contract.functions.swapExactETHForTokens(
        0, # set to 0 for indefinite, or specify minimum amount to receive - Decimals matter Here.
        [spend,toke_to_buy],
        address,
        (int(time.time() + 10000))
        )


    SWP_txn = SWP_txn.build_transaction({
            'from': address,
            'value': web3.to_wei(buy_amount,'ether'),#Token(BNB) amount you will use to swap
            'gas': 250000,
            'gasPrice': gas_price,
            'nonce': nonce,
            })

    signed_txn = web3.eth.account.sign_transaction(SWP_txn, private_key=wallet._private_key)
    try:
        tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        web3.eth.wait_for_transaction_receipt(tx_token, timeout=900)
        trans_hash = web3.to_hex(tx_token)
        print('Done. trx_hash=>',trans_hash)
        return trans_hash
    except:
        print("error **"*5)
        return "error"





############################################################
############################################################
def get_token_balance(MyAddress,_contract,web3):
    my_address = web3.to_checksum_address(MyAddress)
    _abi = get_abi(_contract,web3)
    contract_object = web3.eth.contract(address=_contract, abi=_abi)
    balance = contract_object.functions.balanceOf(my_address).call()
    balance = web3.from_wei(balance, 'ether')
    return balance


############################################################
############################################################
def approve_token(wallet,token_value,token_address,router_address,web3):
    try:
        _abi = get_abi(token_address,web3)
        _contract = web3.eth.contract(address=token_address, abi=_abi)
        address = wallet._address
        nonce = web3.eth.get_transaction_count(address)
        gas_price = web3.eth.gas_price

        approve = _contract.functions.approve(router_address, web3.to_wei(token_value,'ether')).build_transaction({
                    'from': wallet._address,
                    'gasPrice': gas_price,
                    'nonce': nonce,
                    })
        signed_txn = web3.eth.account.sign_transaction(approve, private_key=wallet._private_key)
        try:
            tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
            web3.eth.wait_for_transaction_receipt(tx_token, timeout=900)
            trans_hash = web3.to_hex(tx_token)
            print("Approved: " + trans_hash)
            return "approved"
        except:
            print("Already been approved.")
            return "approved"
    except:
        print("Error in approve function.")
        return "error"



############################################################
############################################################
def swap_token_for_eth(wallet,sell_amount,toke_to_sell,spend,router_contract,web3):
    address = wallet._address
    nonce = web3.eth.get_transaction_count(address)
    gas_price = web3.eth.gas_price

    SWP_txn = router_contract.functions.swapExactTokensForETH(
        web3.to_wei(sell_amount,'ether'),
        1, # set to 0 for indefinite, or specify minimum amount to receive - Decimals matter Here.
        [toke_to_sell,spend],
        address,
        (int(time.time() + 10000))
        )

    SWP_txn = SWP_txn.build_transaction({
            'from': address,
            'gas': 250000,
            'gasPrice': gas_price,
            'nonce': nonce,
            })

    signed_txn = web3.eth.account.sign_transaction(SWP_txn, private_key=wallet._private_key)
    try:
        tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        web3.eth.wait_for_transaction_receipt(tx_token, timeout=900)
        trans_hash = web3.to_hex(tx_token)
        print('Done. trx_hash=>',trans_hash)
        return trans_hash
    except:
        print("error **"*5)
        return "error"


############################################################
############################################################
def sell_token_for_eth(wallet,sell_amount,toke_to_sell,spend,router_contract,web3):    
    approved = approve_token(wallet,sell_amount,toke_to_sell,router_contract.address,web3)
    if approved=="approved":
        time.sleep(3)
        trans_hash = swap_token_for_eth(wallet,sell_amount,
                                        toke_to_sell,spend,
                                        router_contract,web3)
        return trans_hash
    return "error"


