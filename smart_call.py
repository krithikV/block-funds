from web3 import Web3

# Replace with your Sepolia node URL
web3 = Web3(Web3.HTTPProvider('https://rpc.sepolia.org'))


if not web3.is_connected():
    raise Exception("Failed to connect to Sepolia node")

# Contract ABI
with open('abi.json') as f:
    contract_abi = f.read()

# Replace with your contract address
contract_address = "0xffd95ae3c8140e905387CAafA788B6f747DBc8b8"
contract = web3.eth.contract(address=contract_address, abi=contract_abi)
def add_asset(value, property_name, from_address, private_key):
    nonce = web3.eth.get_transaction_count(from_address)
    txn = contract.functions.addAsset(value, property_name).build_transaction({
            'chainId': web3.eth.chain_id,  # Mainnet chain ID
            'gas': 1000000,  # Adjust gas according to the complexity of the function
            'gasPrice': web3.eth.gas_price,
            'nonce': web3.eth.get_transaction_count(from_address),
        })
    signed_txn = web3.eth.account.sign_transaction(txn, private_key=private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    return tx_hash

def get_assets(participant):
    return contract.functions.getAssets(participant).call()

def check_balance():
    return contract.functions.checkBalance().call()

def check_total_balance():
    return contract.functions.checkTotalBalance().call()

def get_deposit_history(participant):
    return contract.functions.getDepositHistory(participant).call()

def deposit(salary, percentage, from_address, private_key):
    nonce = web3.eth.get_transaction_count(from_address)
    txn = contract.functions.deposit(salary, percentage).build_transaction({
            'chainId': web3.eth.chain_id,  # Mainnet chain ID
            'gas': 1000000,  # Adjust gas according to the complexity of the function
            'gasPrice': web3.eth.gas_price,
            'nonce': web3.eth.get_transaction_count(from_address),
        })
    signed_txn = web3.eth.account.sign_transaction(txn, private_key=private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    return tx_hash

def withdraw(amount, from_address, private_key):
    nonce = web3.eth.get_transaction_count(from_address)
    txn = contract.functions.withdraw(amount).build_transaction({
            'chainId': web3.eth.chain_id,  # Mainnet chain ID
            'gas': 1000000,  # Adjust gas according to the complexity of the function
            'gasPrice': web3.eth.gas_price,
            'nonce': web3.eth.get_transaction_count(from_address),
        })
    signed_txn = web3.eth.account.sign_transaction(txn, private_key=private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    return tx_hash

def register_participant(from_address, private_key):
    nonce = web3.eth.get_transaction_count(from_address)
    txn = contract.functions.registerParticipant().build_transaction({
            'chainId': web3.eth.chain_id,  # Mainnet chain ID
            'gas': 1000000,  # Adjust gas according to the complexity of the function
            'gasPrice': web3.eth.gas_price,
            'nonce': web3.eth.get_transaction_count(from_address),
        })
    signed_txn = web3.eth.account.sign_transaction(txn, private_key=private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    return tx_hash

def transfer_asset(to, index, from_address, private_key):
    nonce = web3.eth.get_transaction_count(from_address)
    txn = contract.functions.transferAsset(to, index).build_transaction({
            'chainId': web3.eth.chain_id,  # Mainnet chain ID
            'gas': 1000000,  # Adjust gas according to the complexity of the function
            'gasPrice': web3.eth.gas_price,
            'nonce': web3.eth.get_transaction_count(from_address),
        })
    signed_txn = web3.eth.account.sign_transaction(txn, private_key=private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    return tx_hash

def owner():
    return contract.functions.owner().call()

def total_balance():
    return contract.functions.totalBalance().call()

def is_participant(participant):
    return contract.functions.isParticipant(participant).call()

def get_total_asset_value(from_address):
    return contract.functions.getTotalAssetValue().call({'from': from_address})

def balances(address):
    return contract.functions.balances(address).call()

def assets(address, index):
    return contract.functions.assets(address, index).call()



