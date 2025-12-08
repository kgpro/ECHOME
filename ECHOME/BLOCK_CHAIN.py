# -*- coding: utf-8 -*-
from web3 import Web3
import time
from django.conf import settings
import os
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ECHOME.settings')

class ChainContract:
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, "contract_info.json")
        with open(file_path ,"r", encoding="utf-8") as f:
            import json
            contract_info = json.load(f)
            contract_address = contract_info["contract_address"]
            self.abi = contract_info["abi"]
        self.rpc_endpoint = settings.RPC_ENDPOINT
        self.private_key = settings.PRIVATE_KEY
        self.wallet_address = settings.WALLET_ADDRESS
        self.contract_address = Web3.to_checksum_address(contract_address if contract_info else settings.CONTRACT_ADDRESS)
        self.w3 = Web3(Web3.HTTPProvider(self.rpc_endpoint))

        self.contract = self.w3.eth.contract(address=self.contract_address, abi=self.abi)

        print(f"Connected: {self.w3.is_connected()}")
        print(f"Current block: {self.w3.eth.block_number}")
        print(f"Chain ID: {self.w3.eth.chain_id}")

    def store_data(self, cid, delay_seconds, done_retry=False):
        try:
            if isinstance(cid, str):
                cid_bytes = cid.encode('utf-8')
            else:
                cid_bytes = cid
            nonce = self.w3.eth.get_transaction_count(self.wallet_address)
            tx = self.contract.functions.store(cid_bytes, int(delay_seconds)).build_transaction({
                'chainId': self.w3.eth.chain_id,
                'gas': 600000,
                'gasPrice': self.w3.eth.gas_price,
                'nonce': nonce
            })

            signed_tx = self.w3.eth.account.sign_transaction(tx, self.private_key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)

            print("\n--- Storage Confirmation ---")
            print(f"Transaction hash: {self.w3.to_hex(tx_hash)}")

            # Decode the transaction input to verify what was stored
            tx = self.w3.eth.get_transaction(tx_hash)
            decoded_input = self.contract.decode_function_input(tx['input'])
            function_args = decoded_input[1]
            print(f"Stored data: '{function_args['cid'].decode('utf-8')}'")

            print("--- End of Confirmation ---\n")

            return receipt
        except Exception as e:
            print(f"Error storing data: {str(e)}")
            if not done_retry:
                print("Retrying...")
                return self.store_data(cid, delay_seconds, done_retry=True)
            else:
                print("Retry failed.")
                return None

    def get_expired_data(self, done_retry=False):
        """Get expired CIDs using .caller for view-only contract interaction"""
        try:
            # Use .caller to call the view function
            cids = self.contract.functions.getExpired().call()
            print(f"Expired CIDs retrieved: {cids}")

            for i in range(len(cids)):
                self.deleteExpired(cids[i])

            return {
                'cids': cids,
                'count': len(cids)
            }

        except Exception as e:
            print(f"Error calling getExpired via caller: {str(e)}")
            if not done_retry:
                print("Retrying...")
                time.sleep(3)
                return self.get_expired_data(done_retry=True)
            return {'expired_ids': [], 'cids': [], 'count': 0}


    def deleteExpired(self, expired_id, done_retry=False):
        try:          # Build and send transaction
            nonce = self.w3.eth.get_transaction_count(self.wallet_address)
            tx = self.contract.functions.expire(expired_id).build_transaction({
                'chainId':self.w3.eth.chain_id,  # Sepolia
                'gas': 600000,
                'gasPrice': self.w3.eth.gas_price,
                'nonce': nonce
            })

            signed_tx = self.w3.eth.account.sign_transaction(tx, self.private_key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            print(f" expired CIDs deleted")
            return receipt

        except Exception as e:
            print(f"Error retrieving expired data: {str(e)}")
            if not done_retry:
                print("Retrying...")
                return self.deleteExpired(expired_id,done_retry=True)


# client = ChainContract()
# # print(client.store_data("QmYwAPJzv5CZsnA625s3Xf2nemtYgPpHdWEz79ojWnPbdG", 10))
# # print(client.store_data("QmYwAPJzv5CZsnA625s3Xf2nemtYgPpHdWEz79ojWnPbdH", 9))
# # time.sleep(15)
# print(client.get_expired_data())

