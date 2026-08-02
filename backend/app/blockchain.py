"""
Handles all interaction with the NurseLicenseRegistry smart contract.
Assumes a local Hardhat node is running (or update RPC_URL for testnet).
"""
from web3 import Web3
import json
import os

RPC_URL = os.getenv("CARECHAIN_RPC_URL", "http://127.0.0.1:8545")
CONTRACT_ADDRESS = os.getenv("CARECHAIN_CONTRACT_ADDRESS", "")

w3 = Web3(Web3.HTTPProvider(RPC_URL))

# Minimal ABI covering the functions the backend calls.
CONTRACT_ABI = json.loads("""
[
  {"inputs":[{"internalType":"address","name":"_nurse","type":"address"}],
   "name":"isLicenseValid","outputs":[{"internalType":"bool","name":"","type":"bool"}],
   "stateMutability":"view","type":"function"},
  {"inputs":[{"internalType":"address","name":"_nurse","type":"address"}],
   "name":"getLicense",
   "outputs":[
     {"internalType":"string","name":"licenseNumber","type":"string"},
     {"internalType":"string","name":"issuingState","type":"string"},
     {"internalType":"uint256","name":"issuedAt","type":"uint256"},
     {"internalType":"uint256","name":"expiresAt","type":"uint256"},
     {"internalType":"bool","name":"isRevoked","type":"bool"},
     {"internalType":"bool","name":"isCurrentlyValid","type":"bool"}
   ],
   "stateMutability":"view","type":"function"}
]
""")


def get_contract():
    if not CONTRACT_ADDRESS:
        raise RuntimeError("CARECHAIN_CONTRACT_ADDRESS is not set. Deploy the contract first.")
    return w3.eth.contract(address=Web3.to_checksum_address(CONTRACT_ADDRESS), abi=CONTRACT_ABI)


def is_nurse_license_valid(wallet_address: str) -> bool:
    """Returns True only if the nurse's on-chain license is verified, not revoked, and not expired."""
    if not wallet_address:
        return False
    contract = get_contract()
    return contract.functions.isLicenseValid(Web3.to_checksum_address(wallet_address)).call()


def get_license_details(wallet_address: str) -> dict:
    contract = get_contract()
    result = contract.functions.getLicense(Web3.to_checksum_address(wallet_address)).call()
    return {
        "license_number": result[0],
        "issuing_state": result[1],
        "issued_at": result[2],
        "expires_at": result[3],
        "is_revoked": result[4],
        "is_currently_valid": result[5],
    }
