from constants import *
import subprocess
import json
import os
from dotenv import load_dotenv
from web3 import Web3
from eth_account import Account
from bit import PrivateKeyTestnet

def derive_wallets(coin, numderive = 3):    
    mnemonic = os.getenv('MNEMONIC', 'require enrich hurry machine address addict current survey fault ready orient general muffin tiny spy')             
    command = f'php derive -g --mnemonic="{mnemonic}" --cols=path,address,privkey,pubkey --format="json" --coin="{coin}" --numderive={numderive}'

    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    p_status = p.wait() 	

    keys = json.loads(output)
    return keys

def priv_key_to_account(coin, priv_key):
    if (coin == ETH):        
        return Account.privateKeyToAccount(priv_key)
    elif (coin == BTCTEST):
        return PrivateKeyTestnet(priv_key)
    else: 
        return None

def create_tx(coin, account, to, amount):
    if (coin == ETH):  
        # ADD CODE TO CREATE A TRANSACTION

        return {
            'to':'',
            'from':'',
            'value':'',
            'gas':'',
            'gasPrice':'',
            'nonce':'',
            'chainID':''
        }
    elif (coin == BTCTEST):
        return PrivateKeyTestnet.prepare_transaction(account.address, [(to, amount, BTC)])
    else: 
        return None

def send_tx(coin, account, to, amount):

    raw_tx = create_tx(coin, account, to, amount)

    # if (coin == ETH):
        # return w3.eth.sendRawTransaction(signed.rawTransaction)        
    # elif (coin == BTCTEST):
        # return NetworkAPI.broadcast_tx_testnet(signed)
    # else: 
        # return None


    return None



# BUILD COIN OBJECT (WITH PRIVATE KEYS) FOR EACH CURRENCY
coins = {}
coins[ETH] = derive_wallets(coin = ETH)
coins[BTCTEST] = derive_wallets(coin = BTCTEST)
# print(coins)

# GET ACCOUNT DETAILS FOR EACH CURRENCY USING PRIVATE KEY
account = {}
account[ETH] = priv_key_to_account(coin = ETH, priv_key = coins[ETH][0]['privkey'])
account[BTCTEST] = priv_key_to_account(coin = BTCTEST, priv_key = coins[BTCTEST][0]['privkey'])

# CREATE & SEND TRANSACTION FOR EACH CURRENCY
tx_amt = 0.000000002
to_address = None

eth_tx = send_tx(coin = ETH, account = account[ETH].address, to = to_address, amount = tx_amt)
print(eth_tx)

btc_tx = send_tx(coin = BTCTEST, account = account[BTCTEST].address, to = to_address, amount = tx_amt)
print(btc_tx)

