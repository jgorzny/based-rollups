import requests
import csv
import os
import time
from dotenv import load_dotenv
from datetime import datetime


load_dotenv()

# Connect to Ethereum node
#DRPC_ENDPOINT = os.getenv("DRPCS") # Use this one for Taiko
DRPC_ENDPOINT = os.getenv("INSCROLL")

print("DRPC: ", DRPC_ENDPOINT)
print("drpc_url connected...")
analysis_id = str(datetime.now())
print("Scroll", str(analysis_id))

slow = False

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
    if slow:
        time.sleep(2)
    end_block_data = get_block_details(end_block)
    if slow:
        time.sleep(2)
    
    

    start_time = int(start_block_data["timestamp"], 16)
    end_time = int(end_block_data["timestamp"], 16)
    
    total_time = end_time - start_time
    block_count = end_block - start_block

    print("Start", start_time, "End", end_time, "Total", total_time)
    
    return total_time / block_count

def main():
    # From experiments
    target_block = 10893587
    first_block = 5283926

    interval = 500

    # CSV file path
    csv_file = "time-data/13-Jan-2025-Scroll-block-intervals-500-infura.csv"

    # Check if file exists to decide whether to write header
    file_exists = os.path.isfile(csv_file)

    # Open the file in append mode
    with open(csv_file, mode="a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["start_block", "end_block", "average_time"])
        
        # Write header only if the file is new
        if not file_exists:
            writer.writeheader()

        # Create intervals of 500 blocks 
        for start_block in range(first_block, target_block, interval):
            end_block = min(start_block + interval, target_block)
            try:
                avg_time = calculate_average_block_time(start_block, end_block)
                print(f"Blocks {start_block} to {end_block}: Average Block Time = {avg_time:.2f} seconds")
                writer.writerow({"start_block": start_block, "end_block": end_block, "average_time": avg_time})
                # Flush the file buffer to ensure the results are written
                file.flush()
            except Exception as e:
                print(f"Error processing blocks {start_block} to {end_block}: {e}")
                break  # Exit the loop on error to avoid repeating failed intervals

    print(f"Results saved to {csv_file}")

if __name__ == "__main__":
    main()
