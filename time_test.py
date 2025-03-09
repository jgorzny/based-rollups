import requests
import csv
import os
from dotenv import load_dotenv


load_dotenv()

# Connect to Ethereum node
INFURA_NODE = os.getenv("INFURA")
print("Infura: ", INFURA_NODE)
print("INFURA_NODE connected...")

def get_block_details(block_number):
    """
    Fetch block details for a given block number from the DRPC endpoint.
    """
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_getBlockByNumber",
        "params": [hex(block_number), True],
        "id": 1
    }
    response = requests.post(INFURA_NODE, json=payload)
    response.raise_for_status()  # Raise an error if the request fails
    return response.json()["result"]

def calculate_average_block_time(start_block, end_block):
    """
    Calculate the average block time for the interval between start_block and end_block.
    """
    start_block_data = get_block_details(start_block)
    end_block_data = get_block_details(end_block)
    
    start_time = int(start_block_data["timestamp"], 16)
    end_time = int(end_block_data["timestamp"], 16)

    print("Eth Start", start_time)
    print("Eth End", end_time)
    
    total_time = end_time - start_time
    block_count = end_block - start_block

    print("Eth Total", total_time)
    
    return total_time / block_count

def main():
    calculate_average_block_time(19945276,19960128) ## matches Taiko test data

if __name__ == "__main__":
    main()
