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
import csv

start_time = datetime.now()
load_dotenv()

# Create an ArgumentParser object
parser = argparse.ArgumentParser(description="CAAW 2025 Scroll Data Trimmer")

### CONFIG FOR DEBUGGING
verbose = False
slow = True
DELAY = 0.5
DELAY_BLOCK = 0.5

#Scroll:
# Commit
# Finalize
# Revert

print("Hello world - CAAW 2025 Scroll trim for incomplete Taiko data")
print("This script processes collected transactions")

#13 Jan 2025 - Trim processed Scroll data
first_commit_file = "data-scroll/processed-all-combined/2025-01-08 19:10:55.415658-2024-10-12 19:20:32.090929-Scroll-0xa13BAF47339d63B743e7Da8741db5456DAc1E556-commit-processed.txt"
new_commit_file = "data-scroll/processed-all-trimmed/13Jan2025-Final-commit.txt"

first_finalize_file = "data-scroll/processed-all-combined/2025-01-09 21:45:33.104953-2024-10-12 19:20:32.090929-Scroll-0xa13BAF47339d63B743e7Da8741db5456DAc1E556-finalize-processed.txt"
new_finalize_file = "data-scroll/processed-all-trimmed/13Jan2025-Final-finalize.txt"

first_revert_file = "data-scroll/processed-all-combined/2025-01-10 14:06:52.427947-2024-10-12 19:20:32.090929-Scroll-0xa13BAF47339d63B743e7Da8741db5456DAc1E556-revert-processed.txt"
new_revert_file =  "data-scroll/processed-all-trimmed/13Jan2025-Final-revert.txt"

last_allowed_block = 21136529 #max(21136529,20160068,21134697,21135049)

trim_processed = True

START_TIME = 0
PROTOCOL_NAME = 1
TO_ADDR = 2
BLOCK_NUM = 3
TX_HASH = 4
TYPE = 5
# The following fields are only used if we're merging processed files.
EOA = 6
GAS_USED = 7
GAS_PRICE = 8
TIMESTAMP = 9
DATE = 10

def process_files(old_file, new_file):
    print("Reading", old_file)
    print("Writing", new_file)
    row_count = 0
    # Reading the CSV file
    with open(old_file, newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        
        # Don't skip the header -- there isn't one. Add back if one is added.
        #next(csvreader, None)
        
        # Loop through each row in the CSV file
        for row in csvreader:
            if verbose:
                print(row)  # Each row is a list of values
            
            exp_start = row[START_TIME]
            protocol_name = row[PROTOCOL_NAME]
            to_addr = row[TO_ADDR] # This is the contract addr
            block_num = row[BLOCK_NUM]
            tx_hash = row[TX_HASH]
            type = row[TYPE]
            new_row_suffix = ""
            if trim_processed:
                eoa = row[EOA]
                gas = row[GAS_USED]
                gas_price = row[GAS_PRICE]
                timestamp = row[TIMESTAMP]
                block_date = row[DATE]
                new_row_suffix = str(eoa) + "," + str(gas) + "," + str(gas_price) + "," + str(timestamp) + "," + block_date

            new_row_prefix = exp_start + "," + protocol_name + "," + to_addr + "," + block_num + "," + tx_hash + "," + type + ","
            new_row = new_row_prefix + new_row_suffix

            if int(block_num) < last_allowed_block + 1:
                write_file(new_file, new_row)

            # We only count these txs and update the total_tx_map now
            row_count = row_count + 1
    print("Total rows:", row_count)

process_files(first_commit_file, new_commit_file)
process_files(first_finalize_file, new_finalize_file)
process_files(first_revert_file, new_revert_file)
