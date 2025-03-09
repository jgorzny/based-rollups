import requests
import csv
import os
import time
from dotenv import load_dotenv


load_dotenv()

# Connect to Ethereum node
DRPC_ENDPOINT = os.getenv("DRPC")
print("DRPC: ", DRPC_ENDPOINT)
print("drpc_url connected...")

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
    response = requests.post(DRPC_ENDPOINT, json=payload)
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
 
    total_time = end_time - start_time
    block_count = end_block - start_block

    print("Start", start_time, "End", end_time, "Total", total_time)
    
    return total_time / block_count

def main():
    # From experiements
    target_block = 538303
    #target_block = 2 # test only
    first_block = 1 # Not zero

    interval = 500
    block_intervals = []
    csv_data = []

    # Create intervals of 500 blocks 
    for start_block in range(first_block, target_block, interval):
        end_block = min(start_block + interval, target_block)
        block_intervals.append((start_block, end_block))
    
    # Calculate average block times for each interval
    for start_block, end_block in block_intervals:
        avg_time = calculate_average_block_time(start_block, end_block)
        print(f"Blocks {start_block} to {end_block}: Average Block Time = {avg_time:.2f} seconds")
        csv_data.append({"start_block": start_block, "end_block": end_block, "average_time": avg_time})

    
    # Save results to a CSV file
    csv_file = "time-data/13-Jan-2025-Taiko-block-intervals.csv"
    with open(csv_file, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["start_block", "end_block", "average_time"])
        writer.writeheader()
        writer.writerows(csv_data)
    
    print(f"Results saved to {csv_file}")

if __name__ == "__main__":
    main()
