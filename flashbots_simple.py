from web3 import Web3
import os
from dotenv import load_dotenv
from eth_account.account import Account
from eth_account.signers.local import LocalAccount
from flashbots import flashbot


load_dotenv()

my_address = os.getenv("PUBLIC_KEY")

private_key = os.getenv("PRIVATE_KEY")
private_key = bytearray.fromhex(private_key.replace("0x", ""))

signer : LocalAccount = Account.from_key(os.getenv("ETH_SIGNER_KEY"))

receiver = "0x9d3936dbd9a794ee31ef9f13814233d435bd806c"
receiver = Web3.to_checksum_address(receiver)

w3 = Web3(Web3.HTTPProvider(os.getenv("PROVIDER_URL")))
flashbot(w3, signer)



nonce = w3.eth.get_transaction_count(Web3.to_checksum_address(my_address))

tx1 = {
        "to": receiver,
        "value": Web3.to_wei(0.001, "ether"),
        "gas": 21000,
        "maxFeePerGas": Web3.to_wei(200, "gwei"),
        "maxPriorityFeePerGas": Web3.to_wei(50, "gwei"),
        "nonce": nonce,
        "chainId": 1,
        "type": 2,
    }
tx1_signed = w3.eth.account.sign_transaction(tx1,private_key=private_key)

tx2 = {
        "to": receiver,
        "value": Web3.to_wei(0.001, "ether"),
        "gas": 21000,
        "maxFeePerGas": Web3.to_wei(200, "gwei"),
        "maxPriorityFeePerGas": Web3.to_wei(50, "gwei"),
        "nonce": nonce,
        "chainId": 1,
        "type": 2,
    }
tx2_signed = w3.eth.account.sign_transaction(tx2,private_key=private_key)

bundle = [
        {"signed_transaction": tx1_signed.rawTransaction},
        {"signed_transaction": tx2_signed.rawTransaction},
    ]

block = w3.eth.block_number
try:
    simulation = w3.flashbots.simulate(bundle, block + 1)
except Exception as e:
    print("Error in simulation", e)

    