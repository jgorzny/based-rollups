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
parser = argparse.ArgumentParser(description="CAAW 2025 Data Checker")

### CONFIG FOR DEBUGGING
verbose = False
slow = True
DELAY = 0.5
DELAY_BLOCK = 0.5

print("Hello world - CAAW 2025 data verification")

datafile = "data-taiko/processed-all-combined/10Jan2025-Final-Propose.txt"

START_TIME = 0
PROTOCOL_NAME = 1
TO_ADDR = 2
BLOCK_NUM = 3
TX_HASH = 4
TYPE = 5
EOA = 6
GAS_USED = 7
GAS_PRICE = 8
TIMESTAMP = 9
DATE = 10

def process_file(file):
    print("Reading", file)
    row_count = 0
    # Reading the CSV file

    countMap = {}
    duplicate_count = 0
    max = 0
    proposals_per_block_map = {}
    num_with_six = []

    with open(file, newline='') as csvfile:
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
            eoa = row[EOA]
            gas = row[GAS_USED]
            gas_price = row[GAS_PRICE]
            timestamp = row[TIMESTAMP]
            block_date = row[DATE]

            if block_num in countMap:
                print("Duplicate found!")
                print(tx_hash)
                print(countMap[block_num])
                print(block_num)
                duplicate_count = duplicate_count + 1 
            else:
                countMap[block_num] = tx_hash
            
            if block_num in proposals_per_block_map:
                proposals_per_block_map[block_num] = proposals_per_block_map[block_num] + 1
                if proposals_per_block_map[block_num] > 2:
                    print("Triplicate found!", block_num)
                if proposals_per_block_map[block_num] > max:
                    print("New max found!", block_num, proposals_per_block_map[block_num])
                    max = proposals_per_block_map[block_num]
            else:
                proposals_per_block_map[block_num] = 1

            if proposals_per_block_map[block_num] == 6:
                num_with_six.append(block_num)

            # We only count these txs and update the total_tx_map now
            row_count = row_count + 1
    print("Total rows:", row_count)
    print("Total dups:", duplicate_count)
    print("Max", max)
    print("Num of 6s:", len(num_with_six))

    
    counts = [0,0,0,0,0,0]
    for block in proposals_per_block_map:
        counts[proposals_per_block_map[block]-1] = counts[proposals_per_block_map[block]-1] + 1
    print("Counts", counts)

    sum = 0
    for i in range(0, len(counts)):
        sum = sum + counts[i]
    zeroes = 1362564 - sum #1362564 is number of blocks in data set
    print("Zeros", zeroes)
    
    #print("Checking triplicates...")
    #for key in proposals_per_block_map.keys:
    #    if proposals_per_block_map[key] > 2:
    #        print(proposals_per_block_map[key])

process_file(datafile)