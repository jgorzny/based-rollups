import csv
from collections import defaultdict

def count_duplicate_entries(files, index):
    entry_counts = defaultdict(set)  # Dictionary to track which files an entry appears in
    
    for file_index, file in enumerate(files):
        with open(file, 'r', newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) > 2:  # Ensure there are enough columns
                    entry_counts[row[index]].add(file_index)  
    
    # Count entries that appear in more than one file
    duplicate_entries = {entry for entry, file_set in entry_counts.items() if len(file_set) > 1}
    
    print("Duplicate Entries:")
    for entry in duplicate_entries:
        print(entry)

    return len(duplicate_entries)

def count_distinct_elements(files, index):
    unique_elements = set()
    
    for file in files:
        with open(file, 'r', newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) > index:  # Ensure index is within bounds
                    unique_elements.add(row[index])
    
    return len(unique_elements)

contest_file = "data-taiko/processed-all-combined/10Jan2025-Final-Contested.txt"
propose_file = "data-taiko/processed-all-combined/10Jan2025-Final-Propose.txt"
prove_file = "data-taiko/processed-all-combined/10Jan2025-Final-Prove.txt"
verify_file = "data-taiko/processed-all-combined/10Jan2025-Final-Verify.txt"


scroll_commit_file = "data-scroll/processed-all-trimmed/13Jan2025-Final-commit.txt"
scroll_finalize_file = "data-scroll/processed-all-trimmed/13Jan2025-Final-finalize.txt"
scroll_revert_file = "data-scroll/processed-all-trimmed/13Jan2025-Final-revert.txt"

index = 4 
csv_files_taiko = [contest_file, propose_file, prove_file, verify_file]
csv_files_scroll = [scroll_commit_file,scroll_finalize_file,scroll_revert_file]
result_taiko = count_duplicate_entries(csv_files_taiko, index)
result_scroll = count_duplicate_entries(csv_files_scroll, index)

distinct_scroll = count_distinct_elements(csv_files_scroll, index)
distinct_taiko = count_distinct_elements(csv_files_taiko, index)

print(f"Number of entries appearing in more than one file (TAIKO): {result_taiko}")
print(f"Number of entries appearing in more than one file (SCROLL): {result_scroll}")

print(f"Number of disinct entries appearing files (TAIKO): {distinct_taiko}")
print(f"Number of disinct entries appearing files (SCROLL): {distinct_scroll}")

duplicate_taiko =  result_taiko / distinct_taiko
duplicate_scroll =  result_scroll / distinct_scroll

print(f"Percent Duplicate (TAIKO): {duplicate_taiko}")
print(f"Percent Duplicate (SCROLL): {duplicate_scroll}")