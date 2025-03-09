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
parser = argparse.ArgumentParser(description="FC V2 Processor")


### CONFIG FOR DEBUGGING
verbose = False
slow = True
DELAY = 0.5
DELAY_BLOCK = 0.5

#Scroll:
# Commit
# Finalize
# Revert

print("Hello world - CAAW 2025 merge for incomplete data")
print("This script processes collected transactions")

# 7 Jan: Merging raw Scroll data
#first_commit_file = "data-scroll/unprocessed-all/2024-10-12 19:20:32.090929-Scroll-0xa13BAF47339d63B743e7Da8741db5456DAc1E556-commit.txt"
#additional_commit_file = "data-scroll/unprocessed-all/2025-01-07 04:44:38.307511-Scroll-0xa13BAF47339d63B743e7Da8741db5456DAc1E556-commit.txt"

#first_finalize_file = "data-scroll/unprocessed-all/2024-10-12 19:20:32.090929-Scroll-0xa13BAF47339d63B743e7Da8741db5456DAc1E556-finalize.txt"
#additional_finalize_file = "data-scroll/unprocessed-all/2025-01-07 04:44:38.307511-Scroll-0xa13BAF47339d63B743e7Da8741db5456DAc1E556-finalize.txt"

#first_revert_file = "data-scroll/unprocessed-all/2024-10-12 19:20:32.090929-Scroll-0xa13BAF47339d63B743e7Da8741db5456DAc1E556-revert.txt"
#additional_revert_file = "data-scroll/unprocessed-all/2025-01-07 04:44:38.307511-Scroll-0xa13BAF47339d63B743e7Da8741db5456DAc1E556-revert.txt"

#10 Jan: Merging processed Scroll data.
#first_commit_file =      "data-scroll/processed-all-not-combined/2025-01-08 19:10:55.415658-2024-10-12 19:20:32.090929-Scroll-0xa13BAF47339d63B743e7Da8741db5456DAc1E556-commit-processed.txt"
#additional_commit_file = "data-scroll/processed-all-not-combined/2025-01-09 14:28:32.571304-2024-10-12 19:20:32.090929-Scroll-0xa13BAF47339d63B743e7Da8741db5456DAc1E556-commit-processed.txt"

#10 Jan: Merging processed Taiko data.
#first_contested_file = "data-taiko/processed-all-combined/10Jan2025-Final-Contested.txt"
#second_contested_file = "" # No need - there isn't any more contested transactions.

first_propose_file = "data-taiko/processed-all-combined/10Jan2025-Final-Propose.txt"
second_propose_file = "data-taiko/processed-from-2025/2025-01-07 21:49:23.191596-2025-01-07 21:30:22.585014-Taiko-0x06a9Ab27c7e2255df1815E6CC0168d7755Feb19a-propose-processed.txt"

first_prove_file = "data-taiko/processed-all-combined/10Jan2025-Final-Prove.txt"
second_prove_file = "data-taiko/processed-from-2025/2025-01-07 21:49:23.191596-2025-01-07 21:30:22.585014-Taiko-0x06a9Ab27c7e2255df1815E6CC0168d7755Feb19a-prove-processed.txt"

first_verify_file = "data-taiko/processed-all-combined/10Jan2025-Final-Verify.txt"
second_verify_file = "data-taiko/processed-from-2025/2025-01-07 21:49:23.191596-2025-01-07 21:30:22.585014-Taiko-0x06a9Ab27c7e2255df1815E6CC0168d7755Feb19a-verify-processed.txt"

merge_processed = True

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
    print("Reading", new_file)
    print("Writing", old_file)
    row_count = 0
    # Reading the CSV file
    with open(new_file, newline='') as csvfile:
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
            if merge_processed:
                eoa = row[EOA]
                gas = row[GAS_USED]
                gas_price = row[GAS_PRICE]
                timestamp = row[TIMESTAMP]
                block_date = row[DATE]
                new_row_suffix = str(eoa) + "," + str(gas) + "," + str(gas_price) + "," + str(timestamp) + "," + block_date

            new_row_prefix = exp_start + "," + protocol_name + "," + to_addr + "," + block_num + "," + tx_hash + "," + type + ","
            new_row = new_row_prefix + new_row_suffix

            write_file(old_file, new_row)

            # We only count these txs and update the total_tx_map now
            row_count = row_count + 1
    print("Total rows:", row_count)

process_files(first_propose_file, second_propose_file)
process_files(first_prove_file, second_prove_file)
process_files(first_verify_file, second_verify_file)
