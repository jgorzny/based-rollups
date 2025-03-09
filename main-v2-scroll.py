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
#from abi import *

start_time = datetime.now()
load_dotenv()


# Create an ArgumentParser object
parser = argparse.ArgumentParser(description="FC V2 Scroll")

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

print("Hello world - FC 2025 V2 main - Scroll TX")
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

# CAAW 2025 Supplmement
start_block = 20866920
end_block = 21525890 #(Dec-31-2024 11:59:59 PM +UTC)

assert(end_block >= start_block)

commit_events = True
revert_events = True
finalize_events = True
contested_events = True

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

print("Adding Scroll...")
scroll_name = "Scroll"
protocol_names.append(scroll_name)
# Contract ABI and address
#contract_abi = scroll_abi
contract_address = "0xa13BAF47339d63B743e7Da8741db5456DAc1E556"
print("Contract address:", contract_address)
# 0x06a9Ab27c7e2255df1815E6CC0168d7755Feb19a Proxy address
smart_contract_addresses_map[contract_address] = scroll_name # from Etherscan; should be formatted.


if verbose:
    print(smart_contract_addresses_map)

print("Protocols added!")
print("protocols:", protocol_names)

headers = {
    'Content-Type': 'application/json',
}

print("Setup completed.")


# event CommitBatch(uint256 indexed batchIndex, bytes32 indexed batchHash);
# From Etherscan https://etherscan.io/tx/0x9ef2c64e6a0fc19d715cd95466dbedf34e4d455fc853b6e0845fec9e07f3bb6e#eventlog
commit_event_signature = "0x2c32d4ae151744d0bf0b9464a3e897a1d17ed2f1af71f7c9a75f12ce0d28238f"
 
# event RevertBatch(uint256 indexed batchIndex, bytes32 indexed batchHash); # Computed manually
revert_event_signature = "0x00cae2739091badfd91c373f0a16cede691e0cd25bb80cff77dd5caeb4710146"

# event FinalizeBatch(uint256 indexed batchIndex, bytes32 indexed batchHash, bytes32 stateRoot, bytes32 withdrawRoot);
# From Etherscan: https://etherscan.io/tx/0x4f0a8ddd3f8b0bc2c5b0c4ab3083ec65d86974409705e56b5ab8fd16e823f983#eventlog
finalize_event_signature = "0x26ba82f907317eedc97d0cbef23de76a43dd6edb563bdb6e9407645b950a7a2d"

# Create the contract instance
#contract = web3.eth.contract(address=contract_address, abi=contract_abi)

if commit_events:
    query_in_batches(web3, delta, start_time, scroll_name, commit_event_signature, start_block, end_block, contract_address, 5)

if revert_events:
    query_in_batches(web3, delta, start_time, scroll_name, revert_event_signature, start_block, end_block, contract_address, 6)

if finalize_events:
    query_in_batches(web3, delta, start_time, scroll_name, finalize_event_signature, start_block, end_block, contract_address, 7)

print("Transactions collected!")

end_time = datetime.now()

print("Finished!")
print("Start time:", start_time)
print("End time:", end_time)
