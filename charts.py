import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd
from datetime import datetime
from chartsutil import *

contest_file = "data-taiko/processed-all-combined/10Jan2025-Final-Contested.txt"
propose_file = "data-taiko/processed-all-combined/10Jan2025-Final-Propose.txt"
prove_file = "data-taiko/processed-all-combined/10Jan2025-Final-Prove.txt"
verify_file = "data-taiko/processed-all-combined/10Jan2025-Final-Verify.txt"

#scroll_commit_file = "data-scroll/processed-all-combined/2025-01-08 19:10:55.415658-2024-10-12 19:20:32.090929-Scroll-0xa13BAF47339d63B743e7Da8741db5456DAc1E556-commit-processed.txt"
#scroll_finalize_file = "data-scroll/processed-all-combined/2025-01-09 21:45:33.104953-2024-10-12 19:20:32.090929-Scroll-0xa13BAF47339d63B743e7Da8741db5456DAc1E556-finalize-processed.txt" 
#scroll_revert_file = "data-scroll/processed-all-combined/2025-01-10 14:06:52.427947-2024-10-12 19:20:32.090929-Scroll-0xa13BAF47339d63B743e7Da8741db5456DAc1E556-revert-processed.txt"

scroll_commit_file = "data-scroll/processed-all-trimmed/13Jan2025-Final-commit.txt"
scroll_finalize_file = "data-scroll/processed-all-trimmed/13Jan2025-Final-finalize.txt"
scroll_revert_file = "data-scroll/processed-all-trimmed/13Jan2025-Final-revert.txt"

# All options
line_costs_eth_block = False
line_costs_eth_day = False
line_costs_eth_day_cumulative = False
stacked_bar_proposer = False
distinct_proposers = False
distinct_provers = False
distinct_verifiers = False
num_blocks_proposed_per_day = False
bar_chart_num_events_emitted = False
bar_chart_num_events_emitted_grouped = False
clustered_distinct = False
line_costs_eth_day_scroll = False
line_costs_eth_day_cumulative_scroll = False
both_cumulative_line_chart = False

# Turn on only (some) paper-included charts
line_costs_eth_day = True 
stacked_distinct_block_proposing_tx_separated = True 
num_blocks_proposed_per_l1_block = True 
line_costs_eth_day_cumulative = False 
scatter_distinct = True 
# Only helpful when Scroll data also exists:
line_costs_eth_day_scroll = True  
both_cumulative_line_chart_all = True 

show_plots = False
output_dir = "results-taiko/"
output_dir_scroll = "results-scroll/"
output_dir_both = "results-both/"
analysis_id = str(datetime.now())

print("Starting at", analysis_id)

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

output_prefix = output_dir + analysis_id + "-"
output_prefix_scroll = output_dir_scroll + analysis_id + "-"
output_prefix_both = output_dir_both + analysis_id + "-"

csv_row_names = ['Experiment Start', 'Protocol Name', 'To Addr', 'Block Num', 
                 'TX Hash', 'Type', 'EOA', 'Gas Used', 'Gas Price', 'Timestamp', 'Date']

if line_costs_eth_block:
    print("Generating graph for line_costs_eth_block")
    output_file = output_prefix + "gas-costs-per-block-Taiko.png"
    title = "Gas used Per Block"
    line_chart_cost(propose_file, prove_file, verify_file, contest_file, csv_row_names, 
                    show_plots, csv_row_names[BLOCK_NUM], csv_row_names[GAS_USED],
                    title, "Block Number", True, output_file)
    
if line_costs_eth_day:
    print("Generating graph for line_costs_eth_day")
    output_file = output_prefix + "gas-costs-per-day-Taiko.png"
    title = "Gas Used Per Day for Taiko"
    line_chart_cost(propose_file, prove_file, verify_file, contest_file, csv_row_names, 
                    show_plots, csv_row_names[DATE], csv_row_names[GAS_USED], 
                    title, "2024 Day (MM-DD)", False, output_file)
    
if line_costs_eth_day_cumulative:
    print("Generating graph for line_costs_eth_day_cumulative")
    output_file = output_prefix + "cumulative-gas-costs-per-day-Taiko.png"
    title = "Cumulative Gas Used for Taiko"
    cumulative_line_chart_cost(propose_file, prove_file, verify_file, contest_file, csv_row_names, output_dir, 
                    show_plots, analysis_id, csv_row_names[DATE], csv_row_names[GAS_USED], 
                    title, "Day", False, output_file)

if stacked_bar_proposer:
    print("Generating graph for stacked_bar_proposer")
    output_file = output_prefix + "stacked-proposer-Taiko.png"
    title = 'Percentage of Transactions by EOA per Day'
    stacked_area_chart(propose_file, show_plots, output_file, csv_row_names, 
                       csv_row_names[DATE], csv_row_names[EOA], title)

if stacked_distinct_block_proposing_tx_separated:
    print("Generating graph for stacked_distinct_block_proposing_tx_separated")
    output_file = output_prefix + "stacked-proposer-tx-separated-Taiko.png"
    title = 'Number of Distinct Block Proposing Events per Day'
    stacked_area_chart_2(propose_file, show_plots, output_file, csv_row_names, 
                       csv_row_names[DATE], csv_row_names[EOA], title)


if distinct_proposers:
    print("Generating graph for distinct_proposers")
    output_file = output_prefix + "bar-distinct-proposers-Taiko.png"
    title = 'Number of Distinct Proposer EOAs with Transactions per Day'
    ylabel = 'Number of Distinct EOAs'
    bar_chart_distinct_per_day(propose_file, show_plots, output_file, csv_row_names, csv_row_names[DATE],
                            csv_row_names[EOA], title, True, ylabel)
    
if distinct_provers:
    print("Generating graph for distinct_provers")
    output_file = output_prefix + "bar-distinct-provers-Taiko.png"
    title = 'Number of Distinct Prover EOAs with Transactions per Day'
    ylabel = 'Number of Distinct EOAs'
    bar_chart_distinct_per_day(prove_file, show_plots, output_file, csv_row_names, csv_row_names[DATE],
                            csv_row_names[EOA], title, True, ylabel)
    
if distinct_verifiers:
    print("Generating graph for distinct_verifiers")
    output_file = output_prefix + "bar-distinct-verifiers-Taiko.png"
    title = 'Number of Distinct Verifier EOAs with Transactions per Day'
    ylabel = 'Number of Distinct EOAs'
    bar_chart_distinct_per_day(verify_file, show_plots, output_file, csv_row_names, csv_row_names[DATE],
                            csv_row_names[EOA], title, True, ylabel)

if num_blocks_proposed_per_day:
    print("Generating graph for num_blocks_proposed_per_day")
    output_file = output_prefix + "bar-distinct-proposing-tx-Taiko.png"
    title = 'Number of Distinct Block Proposing Transactions per Day'
    ylabel = 'Number of Transactions'
    bar_chart_distinct_per_day(propose_file, show_plots, output_file, csv_row_names, csv_row_names[DATE],
                            csv_row_names[TX_HASH], title, False, ylabel)

if bar_chart_num_events_emitted:
    print("Generating graph for bar_chart_num_events_emitted")
    files = [propose_file, contest_file, prove_file, verify_file]
    labels = ["BlockProposed", "TransitionContested", "TransitionProved", "BlockVerified"]
    output_file = output_prefix + "bar-num-events-emitted-Taiko.png"
    num_events_emitted(files, labels, output_file, show_plots, csv_row_names)

if bar_chart_num_events_emitted_grouped:
    print("Generating graph for bar_chart_num_events_emitted_grouped")
    files = [propose_file, contest_file, prove_file, verify_file, 
             scroll_commit_file, scroll_revert_file, scroll_finalize_file]
    labels = ["BlockProposed", "TransitionContested", "TransitionProved", "BlockVerified",
              "CommitBatch", "RevertBatch", "FinalizeBatch"]
    output_file = output_prefix_both + "bar-num-events-emitted-grouped-Both.png"
    num_events_emitted_grouped(files, labels, output_file, show_plots, csv_row_names)

if num_blocks_proposed_per_l1_block:
    print("Generating graph for num_blocks_proposed_per_l1_block")
    output_file = output_prefix + "bar-distinct-proposing-tx-per-l1-block-Taiko.png"
    title = 'Number of Block Proposal Events per L1 Block'
    ylabel = 'Number of Events'
    scatter_plot_distinct_per_block(propose_file, show_plots, output_file, csv_row_names, csv_row_names[BLOCK_NUM],
                            csv_row_names[TX_HASH], title, False, ylabel)
    
if clustered_distinct:
    print("Generating graph for clustered_distinct")
    data_files = [propose_file, prove_file, verify_file]
    output_file = output_prefix + 'clustered-distinct-Taiko.png'
    title='Distinct EOAs per Day'
    ylabel='Number of EOAs'
    labels = ["Proposers", "Provers", "Verifiers"]
    clustered_bar_chart(data_files, show_plots, output_file, csv_row_names,
                    csv_row_names[DATE],  csv_row_names[EOA], title, True, ylabel, labels)

# Scroll only 
if line_costs_eth_day_scroll:
    print("Generating graph for line_costs_eth_day_scroll")
    output_file = output_prefix_scroll + "gas-costs-per-day-Scroll.png"
    title = "Gas Used Per Day for Scroll"
    line_chart_cost_scroll(scroll_commit_file, scroll_revert_file, scroll_finalize_file, csv_row_names, 
                    show_plots, csv_row_names[DATE], csv_row_names[GAS_USED], 
                    title, "2024 Day (MM-DD)", False, output_file)
    
if line_costs_eth_day_cumulative_scroll:
    print("Generating graph for line_costs_eth_day_cumulative_scroll")
    output_file = output_prefix_scroll + "cumulative-gas-costs-per-day-Scroll.png"
    title = "Cumulative Gas Used for Scroll"
    cumulative_line_chart_cost_scroll(scroll_commit_file, scroll_revert_file, scroll_finalize_file, csv_row_names,  
                    show_plots, csv_row_names[DATE], csv_row_names[GAS_USED], 
                    title, "Day", False, output_file)    
    
if both_cumulative_line_chart:
    print("Generating graph for both_cumulative_line_chart")
    output_file = output_prefix_both + "cumulative-only-gas-costs-per-day-Both.png"
    title="Cumulative Gas Usage for Scroll and Taiko"
    combined_cumulative_costs_chart_man(
        propose_file,
        prove_file,
        verify_file,
        contest_file,
        scroll_commit_file,
        scroll_revert_file,
        scroll_finalize_file,
        csv_row_names,
        show_plots,
        csv_row_names[DATE],
        csv_row_names[GAS_USED],
        title,
        "Day",
        False,
        output_file)
    
if scatter_distinct:
    print("Generating graph for scatter_distinct")
    data_files = [propose_file, prove_file, verify_file]
    output_file = output_prefix + 'scatter-distinct-Taiko.png'
    title='Distinct EOAs per Day'
    ylabel='Number of EOAs'
    labels = ["Proposers (BlockProposed)", "Provers (TransitionProved)", "Verifiers (BlockVerified)"]
    clustered_scatter_plot(data_files, show_plots, output_file, csv_row_names,
                    csv_row_names[DATE],  csv_row_names[EOA], title, True, ylabel, labels)
    

#### 17 Jan 2025
    
if both_cumulative_line_chart_all:
    print("Generating graph for both_cumulative_line_chart_all")
    output_file = output_prefix_both + "cumulative-only-gas-costs-per-day-all-Both.png"
    title="Cumulative Gas Usage for Scroll and Taiko"
    combined_cumulative_costs_chart_man_all(
        propose_file,
        prove_file,
        verify_file,
        contest_file,
        scroll_commit_file,
        scroll_revert_file,
        scroll_finalize_file,
        csv_row_names,
        show_plots,
        csv_row_names[DATE],
        csv_row_names[GAS_USED],
        title,
        "2024 Day (MM-DD)",
        False,
        output_file)
    

print("Finished at", str(datetime.now()))
