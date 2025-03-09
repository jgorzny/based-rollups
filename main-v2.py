from web3 import Web3
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import os
import time
from dotenv import load_dotenv
import requests
import json
import argparse
from util import *
from abi import *

start_time = datetime.now()
load_dotenv()


# Create an ArgumentParser object
parser = argparse.ArgumentParser(description="CAAW V2")

# Define arguments
parser.add_argument("--start", type=int, default=19773965, help="The block to start on")  # Positional argument
# The start argument shoud be last one displayed in the output of the console, OR
# one more than the value in the log file

# Parse the arguments
args = parser.parse_args()
input_start_block = args.start
# Access the arguments
print(f"start_block inputted: {input_start_block}")



### CONFIG FOR DEBUGGING
verbose = True
slow = False
DELAY = 0
DELAY_BLOCK = 0.5

print("Hello world - CAAW 2025 V2 main")
print("This script now only collects transactions that emit the relevant events.")

# Connect to Ethereum node
infura_url = os.getenv("INFURA")
print("INFURA: ", infura_url)
web3 = Web3(Web3.HTTPProvider(infura_url))
print("Infura connected...")

### Setup global constants

#Real test
# 20885443 has a propose block
# 20885444 has a prove block
#start_block = 20885442
#end_block = 20885445

#Real data - about 2 months: 19773965 #May-01-2024 08:03:47 AM UTC
#start_block = input_start_block # defaults to 19773965
#end_block = 20215112 #Jul-01-2024 11:59:59 PM +UTC

#Real data - continues from above
#start_block = 20215113 #Jul-02-2024 12:00:11 AM +UTC
#end_block = 20866919 #Oct-01-2024 12:00:11 AM +UT

#Real data - Contract launch to 1 Oct 2024: 19773965 #May-01-2024 08:03:47 AM UTC
#start_block = input_start_block # defaults to 19773965
#end_block = 20866919 #Oct-01-2024 12:00:11 AM +UT

# Check prove data
#start_block = 20866917
#end_block = 20866919

# Check verify data
#start_block = 20866899
#end_block = 20866919

# After FC submission test
#start_block = 20866919
#end_block = 20866920
### works

# CAAW data supplement

start_block = 20866920
end_block = 21525890 #(Dec-31-2024 11:59:59 PM +UTC)

assert(end_block >= start_block)

propose_events = False
prove_events = False
verify_events = True
contested_events = False

delta = 500

useEnds = True
if useEnds:
    block_list = list(range(start_block, end_block))
else:
    block_list = [20587642, 20590951] # update this as appropriate; should be increasing!
    start_block = block_list[0]
    end_block = block_list[len(block_list)-1]   
num_blocks = len(block_list)

print("Going from block " + str(start_block) + " to " + str(end_block) + " (" + str(num_blocks) + ")")

# Log files
block_tracking_file_name = "logs/" + str(start_time) + "-blocks-processed.txt"

# Data
protocol_names = []

smart_contract_addresses_map = {}

print("Adding protocols...")
## Add protocols

print("Adding Taiko...")
taiko_name = "Taiko"
protocol_names.append(taiko_name)
# Contract ABI and address
contract_abi = taiko_abi
contract_address = "0x06a9Ab27c7e2255df1815E6CC0168d7755Feb19a"
print("Contract address:", contract_address)
# 0x06a9Ab27c7e2255df1815E6CC0168d7755Feb19a Proxy address
smart_contract_addresses_map[contract_address] = taiko_name # from Etherscan; should be formatted.
#proposeBlock (0xef16e845), proveBlock (0x10d008bd), verifyBlocks (0x8778209d)


if verbose:
    print(smart_contract_addresses_map)

print("Protocols added!")
print("protocols:", protocol_names)

headers = {
    'Content-Type': 'application/json',
}

print("Setup completed.")


#     event BlockProposed(
#        uint256 indexed blockId,
#        address indexed assignedProver,
#        uint96 livenessBond,
#        TaikoData.BlockMetadata meta,
#        TaikoData.EthDeposit[] depositsProcessed
#    );
# From Etherscan
propose_event_signature_hash = "0xcda4e564245eb15494bc6da29f6a42e1941cf57f5314bf35bab8a1fca0a9c60a"

#    event TransitionProved(
#        uint256 indexed blockId,
#        TaikoData.Transition tran,
#        address prover,
#        uint96 validityBond,
#        uint16 tier
#    );
# From Etherscan
prove_event_signature_hash = "0xc195e4be3b936845492b8be4b1cf604db687a4d79ad84d979499c136f8e6701f"

#    event BlockVerified(
#        uint256 indexed blockId,
#        address indexed prover,
#        bytes32 blockHash,
#        bytes32 stateRoot,
#        uint16 tier
#    );
# From Etherscan # https://etherscan.io/tx/0x82982e06af539384475ab279da2536b43b37afc6da2ec9ab570ae876ea54ae8b#eventlog
verify_event_signature_hash = "0xdecbd2c61cbda254917d6fd4c980a470701e8f9f1b744f6ad163ca70ca5db289"


#    event TransitionContested(
#        uint256 indexed blockId,
#        TaikoData.Transition tran,
#        address contester,
#        uint96 contestBond,
#        uint16 tier
#    );
# From Etherscan: https://etherscan.io/tx/0x7600471694620e19c3296a4e26fc753149cbcd9803f37747521aa3399261ced8#eventlog
contested_event_signature_hash = "0xb4c0a86c1ff239277697775b1e91d3375fd3a5ef6b345aa4e2f6001c890558f6"



# Create the contract instance
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

if propose_events:
    query_in_batches(web3, delta, start_time, taiko_name, propose_event_signature_hash, start_block, end_block, contract_address, 1)

if prove_events:
    query_in_batches(web3, delta, start_time, taiko_name, prove_event_signature_hash, start_block, end_block, contract_address, 2)

if verify_events:
    query_in_batches(web3, delta, start_time, taiko_name, verify_event_signature_hash, start_block, end_block, contract_address, 3)

if contested_events:
    query_in_batches(web3, delta, start_time, taiko_name, contested_event_signature_hash, start_block, end_block, contract_address, 4)


print("Transactions collected!")

#logs = propose_logs + prove_logs

#print("LOGS:")
#print(logs)
# Process the logs
#for log in logs:
#    transaction_hash = log['transactionHash'].hex()
#    # The log does not have to, from, or anything else for a transaction. 
#    # Need to process each transacation separately.
#    
#    print(f"Transaction {transaction_hash}:")


end_time = datetime.now()

print("Finished!")
print("Start time:", start_time)
print("End time:", end_time)

## After this file completes, run `analyse.py` after putting in the right data file names.