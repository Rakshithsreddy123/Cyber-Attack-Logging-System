from web3 import Web3
import hashlib
import json
from config import RPC_URL, CONTRACT_ADDRESS

w3 = Web3(Web3.HTTPProvider(RPC_URL))

with open("contract_abi.json") as f:
    abi = json.load(f)

contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=abi)

def hash_log(log):
    return hashlib.sha256(log.encode()).hexdigest()

def get_contract():
    return contract

def get_web3():
    return w3