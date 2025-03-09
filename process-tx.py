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
import csv

start_time = datetime.now()
load_dotenv()


# Create an ArgumentParser object
parser = argparse.ArgumentParser(description="FC V2 Processor")

process_taiko = False # If false, we process Scroll transactions

#data_dir = "data/"
data_dir = "data-scroll/"

### CONFIG FOR DEBUGGING
verbose = True
slow = True
DELAY = 0.5
DELAY_BLOCK = 0.5
last_confirmed_block = 0 # 0 means all tx will be processed

print("Hello world - CAAW 2025 processor")
print("This script processes collected transactions")

# Connect to Ethereum node
infura_url = os.getenv("INFURA")
print("INFURA: ", infura_url)
web3 = Web3(Web3.HTTPProvider(infura_url))
print("Infura connected...")


# See FC2025 version of this file for sample data.
#main_exp_string = "2025-01-07 21:30:22.585014-Taiko-0x06a9Ab27c7e2255df1815E6CC0168d7755Feb19a"
main_exp_string = "2024-10-12 19:20:32.090929-Scroll-0xa13BAF47339d63B743e7Da8741db5456DAc1E556"

propose_files = []
if process_taiko:
    propose_files.append(data_dir + main_exp_string + "-propose.txt") #Taiko
    new_propose_file = data_dir + str(start_time) + "-" + main_exp_string + "-propose-processed.txt" #Taiko
else:
    propose_files.append(data_dir + main_exp_string + "-commit.txt") #Scroll
    new_propose_file = data_dir + str(start_time) + "-" + main_exp_string + "-commit-processed.txt" #Scroll
#new_propose_file = "data/propose-to-append.txt"
last_confirmed_block = 19867504 ## 8 Jan 2025 

prove_files = []
if process_taiko:
    prove_files.append(data_dir + main_exp_string + "-prove.txt") #Taiko
    new_prove_file = data_dir + str(start_time) + "-" + main_exp_string + "-prove-processed.txt" #Taiko
else:
    prove_files.append(data_dir + main_exp_string + "-finalize.txt") #Scroll
    new_prove_file = data_dir + str(start_time) + "-" + main_exp_string + "-finalize-processed.txt" #Scroll

verify_files = []
if process_taiko:
    verify_files.append(data_dir + main_exp_string + "-verify.txt") #Taiko
    new_verify_file = data_dir + str(start_time) + "-" + main_exp_string + "-verify-processed.txt" #Taiko
else:
    verify_files.append(data_dir+ main_exp_string + "-revert.txt") #Scroll
    new_verify_file = data_dir + str(start_time) + "-" + main_exp_string + "-revert-processed.txt" #Scroll
#new_propose_file = "data/verify-to-append.txt"
#last_confirmed_block = 20589974

contest_files = []
if process_taiko: #Taiko only
    contest_files.append(data_dir+ main_exp_string + "-contested.txt")
    new_contest_file = data_dir + str(start_time) + "-" + main_exp_string + "-contested-processed.txt"

START_TIME = 0
PROTOCOL_NAME = 1
TO_ADDR = 2
BLOCK_NUM = 3
TX_HASH = 4
TYPE = 5

def process_files(filelist, new_file):
    for file in filelist:
        print("Reading", file)
        row_count = 0
        # Reading the CSV file
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

                if int(block_num) > last_confirmed_block: 
                    new_row_prefix = exp_start + "," + protocol_name + "," + to_addr + "," + block_num + "," + tx_hash + "," + type + ","
            
                    (eoa, gas, gas_price, timestamp, block_date) = process_tx2(web3, slow, DELAY, tx_hash)

                    new_row = new_row_prefix + str(eoa) + "," + str(gas) + "," + str(gas_price) + "," + str(timestamp) + "," + block_date

                    write_file(new_file, new_row)

                # We only count these txs and update the total_tx_map now
                row_count = row_count + 1
        print("Total rows:", row_count)

if process_taiko:
    process_files(propose_files, new_propose_file) 
    process_files(prove_files, new_prove_file) 
    process_files(verify_files, new_verify_file)
    #process_files(contest_files, new_contest_file) # None in post-FC data collection.
else:
    process_files(propose_files, new_propose_file) # Actually commit for Scroll
    #process_files(prove_files, new_prove_file) # Actually finalize for Scroll
    #process_files(verify_files, new_verify_file) # Actually revert for Scroll
    #process_files(contest_files, new_contest_file) # N/A for Scroll 

end_time = datetime.now()
print("Started:", start_time)
print("Ended:", end_time)