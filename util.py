from datetime import datetime
import time
from web3.exceptions import Web3RPCError

def append_num_to_file(filename, number):
    with open(filename, "a") as file:
        file.write(str(number) + "\n")

START_TIME = 0
PROTOCOL_NAME = 1
TO_ADDR = 2
BLOCK_NUM = 3
TX_HASH = 4

def record_tx(start_time, protocol_name, block_num, tx_hash, to_addr, opt):
    filename_base = "data/" + str(start_time) + "-" + str(protocol_name) + "-" + str(to_addr) 
    entry = str(start_time)+","+str(protocol_name)+","+str(to_addr)+","+str(block_num)+","+str(tx_hash)

    if opt == 1: # propose
        filename = filename_base + "-propose.txt"
        write_file(filename, entry+",propose")
    elif opt == 2: # prove
        filename = filename_base + "-prove.txt"
        write_file(filename, entry+",prove")
    elif opt == 3: # verify 
        filename = filename_base + "-verify.txt"
        write_file(filename, entry+",verify")
    elif opt == 4: # contested 
        filename = filename_base + "-contested.txt"
        write_file(filename, entry+",contested")

    elif opt == 5: # commit 
        filename = filename_base + "-commit.txt"
        write_file(filename, entry+",commit")
    elif opt == 6: # revert 
        filename = filename_base + "-revert.txt"
        write_file(filename, entry+",revert")
    elif opt == 7: # finalize 
        filename = filename_base + "-finalize.txt"
        write_file(filename, entry+",finalize")

    else: # other -- likely error, but let's not waste the API call
        filename = filename_base + "-other.txt"
        write_file(filename, entry+",other")

def write_file(filename, entry):
    with open(filename, "a") as file:
        file.write(entry + "\n")


def build_block_payload(block_number):
    payload = {
        "jsonrpc": "2.0",
        "method": "trace_block",
        "params": [block_number],  # You can add trace options in the second param (like `tracer`)
        "id": 1
    }
    return payload

def build_tx_payload(transaction_hash):
    payload = {
        "jsonrpc": "2.0",
        "method": "trace_transaction",
        "params": [transaction_hash], 
        "id": 1
    }
    return payload

def query_in_batches(web3, delta, start_time, taiko_name, event_signature, start_block, end_block, contract_address, opt):
    assert(delta > 0)
    temp_start_block = start_block
    temp_end_block = temp_start_block + delta - 1

    #print("S temp_start_block", temp_start_block) # Debug only
    #print("S temp_end_block", temp_end_block) # Debug only

    while temp_start_block <= end_block:
        #print("Looping...")
        if temp_end_block > end_block:
            temp_end_block = end_block

        #print("M temp_start_block", temp_start_block) # Debug only
        #print("M temp_end_block", temp_end_block) # Debug only

        temp_logs = web3.eth.get_logs({
            'fromBlock': temp_start_block,
            'toBlock': temp_end_block,
            'address': contract_address,
            'topics': [event_signature]
        })

        #print("PROPOSE:")
        #print(propose_logs)

        # Process the logs
        for temp_log in temp_logs:
            transaction_hash = temp_log['transactionHash'].hex()
            block_num = temp_log['blockNumber']
            record_tx(start_time, taiko_name, block_num, transaction_hash, contract_address, opt)
            
            print(f"Transaction {transaction_hash}")

        temp_start_block = temp_start_block + delta
        temp_end_block = temp_end_block + delta
    
    #print("E temp_start_block", temp_start_block) # Debug only
    #print("E temp_end_block", temp_end_block) # Debug only
        
def process_tx(web3, slow, DELAY, tx_hash):
    # Get transaction details
    transaction = web3.eth.get_transaction(tx_hash)
    eoa = transaction['from']  # EOA that initiated the transaction
    gas_price = transaction['gasPrice']

    # Get transaction receipt to obtain the gas used
    receipt = web3.eth.get_transaction_receipt(tx_hash)
    gas_used = receipt['gasUsed']  # Gas used by the transaction
    block_number = receipt['blockNumber']

    block = web3.eth.get_block(block_number)
    block_timestamp = block['timestamp']  # Unix timestamp

    # Step 3: Convert the Unix timestamp to a human-readable date
    #block_date = datetime.utcfromtimestamp(block_timestamp).strftime('%Y-%m-%d %H:%M:%S')
    block_date = datetime.utcfromtimestamp(block_timestamp).strftime('%Y-%m-%d')

    # Output the result


    # Print the results
    #print(f"EOA that initiated the transaction: {eoa}")
    #print(f"Gas used in the transaction: {gas_used}")
    print(f"Transaction was processed on: {block_date} UTC")


    return(eoa, gas_used, gas_price, block_timestamp, block_date)


def retry_until_success_tx(web3, slow, delay, opt, tx_hash):
    checked = False
    while not checked:
        try:
            if opt == 1: #
                    transaction = web3.eth.get_transaction(tx_hash)
                    return transaction
            elif opt == 2: #
                    transaction = web3.eth.get_transaction_receipt(tx_hash)
                    return transaction
            else:
                print("Bad option for retry_until_success_tx")
                return None
        except Web3RPCError as e:
            print(f"Attempt failed with error: {e}")
            if slow:
                time.sleep(delay)

def retry_until_success_block(web3, slow, delay, block_num):
    checked = False
    while not checked:
        try:
            block = web3.eth.get_block(block_num)
            return block
        except Web3RPCError as e:
            print(f"Attempt failed with error: {e}")
            if slow:
                time.sleep(delay)

def process_tx2(web3, slow, delay, tx_hash):
    # Get transaction details
    transaction = retry_until_success_tx(web3, slow, delay, 1, tx_hash)
    eoa = transaction['from']  # EOA that initiated the transaction
    gas_price = transaction['gasPrice']

    # Get transaction receipt to obtain the gas used
    receipt = transaction = retry_until_success_tx(web3, slow, delay, 2, tx_hash)
    # web3.eth.get_transaction_receipt(tx_hash)
    gas_used = receipt['gasUsed']  # Gas used by the transaction
    block_number = receipt['blockNumber']

    block = retry_until_success_block(web3, slow, delay, block_number)
    block_timestamp = block['timestamp']  # Unix timestamp

    # Step 3: Convert the Unix timestamp to a human-readable date
    #block_date = datetime.utcfromtimestamp(block_timestamp).strftime('%Y-%m-%d %H:%M:%S')
    block_date = datetime.utcfromtimestamp(block_timestamp).strftime('%Y-%m-%d')

    # Print the results
    #print(f"EOA that initiated the transaction: {eoa}")
    #print(f"Gas used in the transaction: {gas_used}")
    print(f"Transaction was processed on: {block_date} UTC")

    return(eoa, gas_used, gas_price, block_timestamp, block_date)
                
