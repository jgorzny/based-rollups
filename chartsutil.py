import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd
import numpy as np
from matplotlib.ticker import ScalarFormatter

plt.rcParams.update({'font.size': 14})


def stacked_area_chart(data_file, show_plots, output_file, csv_row_names, group_by, data, title):
    # Step 1: Load the CSV file into a pandas DataFrame
    # The CSV contains columns 'eoa', 'tx', 'date'
    df = pd.read_csv(data_file, header=None, names=csv_row_names)

    # Step 2: Convert the 'date' column to datetime
    #df['date'] = pd.to_datetime(df['date'])

    # Step 3: Group by 'date' and 'eoa', and count the number of transactions per EOA per day
    grouped = df.groupby([group_by, data]).size().unstack(fill_value=0)

    # Step 4: Normalize the data to get percentages (100% stacked)
    grouped_percent = grouped.div(grouped.sum(axis=1), axis=0) * 100

    # Step 5: Plot the 100% stacked area bar chart
    grouped_percent.plot(kind='bar', stacked=True, figsize=(90, 22), width=1.0, colormap='tab20')

    # Step 6: Customize the chart
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel('Percentage of Events (%)')
    plt.legend(title='EOA', bbox_to_anchor=(1.05, 1), loc='upper left')

    #plt.tight_layout()  # Adjust layout to prevent label cutoff
    plt.savefig(output_file)

    # Step 7: Show the plot
    if show_plots:
        plt.show()

    plt.clf()

# This version is not percentages.
def stacked_area_chart_2(data_file, show_plots, output_file, csv_row_names, group_by, data, title):
    # Step 1: Load the CSV file into a pandas DataFrame
    # The CSV contains columns 'eoa', 'tx', 'date'
    df = pd.read_csv(data_file, header=None, names=csv_row_names)

    # Step 2: Group by 'date' and 'eoa', and count the number of transactions per EOA per day
    grouped = df.groupby([group_by, data]).size().unstack(fill_value=0)

    # Convert the index to datetime format and extract only MM-DD
    grouped.index = pd.to_datetime(grouped.index).strftime('%m-%d')

    # Step 2.1: Calculate statistics
    num_group_by_elements = len(grouped)
    total_events = grouped.sum().sum()
    sum_per_group = grouped.sum(axis=1)  # Sum of events per group_by entry (e.g., per day)
    largest_group_events = sum_per_group.max()
    percentage_largest_group = (largest_group_events / total_events) * 100
    average_bar_height = sum_per_group.mean()
    max_bar_height = sum_per_group.max()
    num_legend_elements = grouped.shape[1]  # Number of columns in 'grouped' corresponds to unique 'data' values
    print(f"Number of elements in the legend: {num_legend_elements}")

    # Print statistics
    print(f"Number of {group_by} elements: {num_group_by_elements}")
    print(f"Percentage of all events from the largest {group_by} entry: {percentage_largest_group:.2f}%")
    print(f"Average bar height: {average_bar_height:.2f}")
    print(f"Maximum bar height: {max_bar_height:.2f}")

    legend_entry = "0x000000633b68f5D8D3a86593ebB815b4663BCBe0" #Taiko Beat
    legend_count = 0
    # Step 2.2: Get the values for the specific legend entry (e.g., a specific 'EOA')
    if legend_entry in grouped.columns:
        values_for_legend_entry = grouped[legend_entry]
        values_for_legend_entry.sum()
        print(type(values_for_legend_entry)) 

        legend_entry_sum = values_for_legend_entry.sum()
        legend_count = legend_count + legend_entry_sum
        print(f"Values for {legend_entry} over all {group_by} categories:")
        print(values_for_legend_entry)
    else:
        print(f"Legend entry '{legend_entry}' not found in the data.")
    print("Legend count:", legend_count)

    total_sum_of_bars = grouped.sum().sum()
    print(f"Total sum of all bars: {total_sum_of_bars}")

    # Step 3: Plot the 100% stacked area bar chart
    bar_width = 0.8 # reduce for skinnier bars
    grouped.plot(kind='bar', stacked=True, figsize=(10,6), width=bar_width, colormap='tab20', legend=False)

    # Step 4: Customize the chart
    plt.title(title)
    plt.xlabel('2024 Date (MM-DD)')
    plt.ylabel('Number of Events')
    #plt.legend(title='EOA', bbox_to_anchor=(1.05, 1), loc='upper left')

    ticks = plt.gca().get_xticks()
    labels = plt.gca().get_xticklabels()

    # Show every second label
    plt.xticks(ticks[::5], labels[::5]) #, rotation=45

    #plt.tight_layout()  # Adjust layout to prevent label cutoff
    plt.tight_layout()  # Adjust layout to prevent label cutoff

    plt.savefig(output_file)

    # Step 7: Show the plot
    if show_plots:
        plt.show()

    plt.clf()

def bar_chart_distinct_per_day(data_file, show_plots, output_file, csv_row_names, group_by, data, title, distinct, ylabel):
    # Step 1: Load the CSV file into a pandas DataFrame
    # The CSV contains columns 'eoa', 'tx', 'date'
    df = pd.read_csv(data_file, header=None, names=csv_row_names)

    # Step 2: Group by 'date' and count the distinct EOAs per date
    if distinct:
        data_per_day = df.groupby(group_by)[data].nunique()
    else:
        data_per_day = df.groupby(group_by)[data].count()

    # Step 3: Plot the bar chart
    plt.figure(figsize=(10, 6))
    data_per_day.plot(kind='bar', color='skyblue')

    # Step 4: Customize the chart
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel(ylabel)
    #plt.xticks(rotation=45)  # Rotate x-axis labels for better readability (doesn't seem to work well in practice)

    # Get current x-ticks and labels
    ticks = plt.gca().get_xticks()
    labels = plt.gca().get_xticklabels()

    # Show every second label
    plt.xticks(ticks[::2], labels[::2]) #, rotation=45

    plt.tight_layout()  # Adjust layout to prevent label cutoff
    plt.savefig(output_file)

    # Step 6: Show the plot
    if show_plots:
        plt.show()

    plt.clf()

# Can be refactored into bar_chart_distinct_per_day with some effort.
def bar_chart_distinct_per_block(data_file, show_plots, output_file, csv_row_names, group_by, data, title, distinct, ylabel):
    # Step 1: Load the CSV file into a pandas DataFrame
    # The CSV contains columns 'eoa', 'tx', 'block_num'
    df = pd.read_csv(data_file, header=None, names=csv_row_names)

    # Step 3: Group by group_by
    if distinct:
        data_per_day = df.groupby(group_by)[data].nunique()
    else:
        data_per_day = df.groupby(group_by)[data].count()

    # Step 4: Plot the bar chart
    plt.figure(figsize=(10, 6))
    #data_per_day.plot(kind='bar', color='black')
    #data_per_day.plot(color='black')
    x = np.arange(len(data_per_day))  # Positions for the bars
    plt.bar(x, data_per_day, color='black')

    plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(integer=True))

    #plt.gca().xaxis.set_major_locator(mticker.MaxNLocator(nbins=200000))  # Reduce the number of x-ticks


    # Step 5: Customize the chart
    plt.title(title)
    plt.xlabel('L1 Block')
    plt.ylabel(ylabel)

    x_labels = data_per_day.index  # Get all x-axis labels (e.g., block numbers)
    tick_positions = np.arange(0, len(x_labels), 20000)
    tick_labels = [x_labels[i] for i in tick_positions]

    # Set the ticks and labels
    plt.xticks(tick_positions, tick_labels, rotation=90)

    plt.tight_layout()  # Adjust layout to prevent label cutoff
    plt.savefig(output_file)

    # Step 6: Show the plot
    if show_plots:
        plt.show()

    plt.clf()


def num_events_emitted(files, labels, output_file, show_plots, csv_row_names):
    # Step 1: Load the three CSV files
    csv1 = pd.read_csv(files[0], header=None, names=csv_row_names)
    csv2 = pd.read_csv(files[1], header=None, names=csv_row_names)
    csv3 = pd.read_csv(files[2], header=None, names=csv_row_names)
    csv4 = pd.read_csv(files[3], header=None, names=csv_row_names)

    # Step 2: Count the number of rows (entries) in each CSV
    count1 = len(csv1)
    count2 = len(csv2)
    count3 = len(csv3)
    count4 = len(csv4)

    # Step 3: Create a list of counts and corresponding labels for the bar chart
    counts = [count1, count2, count3, count4]

    # Step 4: Create the bar chart
    plt.figure(figsize=(8, 6))
    bars = plt.bar(labels, counts, color=['skyblue', 'red', 'orange', 'green'])

    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, int(yval), ha='center', va='bottom')

    # Step 5: Customize the chart
    plt.title('Number of Events Emitted')
    plt.xlabel('Event')
    plt.ylabel('Number of Emissions')

    # Step 6: Show the plot
    plt.tight_layout()
    plt.savefig(output_file)

    if show_plots:
        plt.show()

    plt.clf()

def cumulative_line_chart_cost(propose_file, prove_file, verify_file, contest_file, csv_row_names, output_dir, show_plots, analysis_id, 
                    group_by, gas_used, title, xlabel, format_x_axis, output_file):
    # Step 1: Load the CSV file into a pandas DataFrame
    df = pd.read_csv(propose_file, header=None, names=csv_row_names)
    df_prove = pd.read_csv(prove_file, header=None, names=csv_row_names)
    df_verify = pd.read_csv(verify_file, header=None, names=csv_row_names)
    df_contest = pd.read_csv(contest_file, header=None, names=csv_row_names)

    # Step 2: Group by 'block_num' and sum the 'gas_used'
    gas_per_block_propose = df.groupby(group_by)[gas_used].sum().reset_index()
    gas_per_block_prove = df_prove.groupby(group_by)[gas_used].sum().reset_index()
    gas_per_block_verify = df_verify.groupby(group_by)[gas_used].sum().reset_index()
    gas_per_block_contest = df_contest.groupby(group_by)[gas_used].sum().reset_index()

    # Step 3: Merge the datasets on 'block_num'
    merged_data = pd.merge(gas_per_block_propose, gas_per_block_prove, on=group_by, how='outer', suffixes=(' (Propose)', ' (Prove)')).fillna(0)
    merged_data = pd.merge(merged_data, gas_per_block_verify, on=group_by, how='outer').fillna(0)
    merged_data.rename(columns={gas_used: 'Gas Used (Verify)'}, inplace=True)
    merged_data = pd.merge(merged_data, gas_per_block_contest, on=group_by, how='outer').fillna(0)
    merged_data.rename(columns={gas_used: 'Gas Used (Contest)'}, inplace=True)

    # Step 4: Calculate the total gas used
    merged_data['Gas Used (Total)'] = (merged_data['Gas Used (Propose)'] + 
                                       merged_data['Gas Used (Prove)'] + 
                                       merged_data['Gas Used (Verify)'] + 
                                       merged_data['Gas Used (Contest)'])

    # Step 5: Calculate cumulative sum for each gas used column
    merged_data['Cumulative Gas Used (Propose)'] = merged_data['Gas Used (Propose)'].cumsum()
    merged_data['Cumulative Gas Used (Prove)'] = merged_data['Gas Used (Prove)'].cumsum()
    merged_data['Cumulative Gas Used (Contest)'] = merged_data['Gas Used (Contest)'].cumsum()
    merged_data['Cumulative Gas Used (Verify)'] = merged_data['Gas Used (Verify)'].cumsum()
    merged_data['Cumulative Gas Used (Total)'] = merged_data['Gas Used (Total)'].cumsum()

    # Step 6: Plot the cumulative data as a line chart
    plt.figure(figsize=(12, 8))  # Increase figure size (width=12, height=8)

    plt.plot(merged_data[group_by], merged_data['Cumulative Gas Used (Propose)'], label="Propose", color='skyblue')
    plt.plot(merged_data[group_by], merged_data['Cumulative Gas Used (Prove)'], label="Prove", color='orange')
    plt.plot(merged_data[group_by], merged_data['Cumulative Gas Used (Contest)'], label="Contest", color='red')
    plt.plot(merged_data[group_by], merged_data['Cumulative Gas Used (Verify)'], label="Verify", color='green')
    plt.plot(merged_data[group_by], merged_data['Cumulative Gas Used (Total)'], label="All", color='black')

    # Step 7: Set custom x-axis ticks (real block numbers)
    plt.xticks(gas_per_block_propose[group_by])

    # Step 8: Customize the plot
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel('Cumulative Gas Used')

    if format_x_axis:
        ax = plt.gca()  # Get current axis
        ax.xaxis.set_major_formatter(mticker.StrMethodFormatter('{x:.0f}'))  # Format x-axis as integer

    ticks = plt.gca().get_xticks()
    labels = plt.gca().get_xticklabels()

    # Show every fourth label
    plt.xticks(ticks[::8], labels[::8], rotation=90)

    plt.legend()
    plt.grid(True)
    plt.tight_layout()  # Adjust layout to prevent label cutoff
    plt.savefig(output_file)

    # Step 9: Show the plot
    if show_plots:
        plt.show()

    plt.clf()




def clustered_bar_chart(data_files, show_plots, output_file, csv_row_names, group_by, data, title, distinct, ylabel, labels):
    # Step 1: Load the CSV files into pandas DataFrames
    df1 = pd.read_csv(data_files[0], header=None, names=csv_row_names)
    df2 = pd.read_csv(data_files[1], header=None, names=csv_row_names)
    df3 = pd.read_csv(data_files[2], header=None, names=csv_row_names)

    # Step 2: Group by 'group_by' and count the distinct EOAs per group
    if distinct:
        data_per_day_1 = df1.groupby(group_by)[data].nunique()
        data_per_day_2 = df2.groupby(group_by)[data].nunique()
        data_per_day_3 = df3.groupby(group_by)[data].nunique()
    else:
        data_per_day_1 = df1.groupby(group_by)[data].count()
        data_per_day_2 = df2.groupby(group_by)[data].count()
        data_per_day_3 = df3.groupby(group_by)[data].count()

    # Step 3: Merge the datasets on 'group_by' to ensure alignment
    merged_data = pd.DataFrame({
        'File 1': data_per_day_1,
        'File 2': data_per_day_2,
        'File 3': data_per_day_3
    }).fillna(0)  # Fill missing values with 0 if any

    # Step 3.1: Calculate and print the average height of each cluster (i.e., average of each dataset)
    avg_file_1 = merged_data['File 1'].mean()
    avg_file_2 = merged_data['File 2'].mean()
    avg_file_3 = merged_data['File 3'].mean()

    max_file_1 = merged_data['File 1'].max()
    max_file_2 = merged_data['File 2'].max()
    max_file_3 = merged_data['File 3'].max()

    print("Max height of " + data_files[0] + " bars:", max_file_1)
    print("Max height of " + data_files[1] + " bars:", max_file_2)
    print("Max height of " + data_files[2] + " bars:", max_file_3)

    print("Average height of " + data_files[0] + " bars:", avg_file_1)
    print("Average height of " + data_files[1] + " bars:", avg_file_2)
    print("Average height of " + data_files[2] + " bars:", avg_file_3)

    # Step 4: Plot the clustered bar chart
    plt.figure(figsize=(10, 6))
    
    # Determine the x locations for the groups
    x = np.arange(len(merged_data.index))
    bar_width = 0.25

    # Plot the bars for each dataset
    plt.bar(x - bar_width, merged_data['File 1'], width=bar_width, label=labels[0], color='skyblue')
    plt.bar(x, merged_data['File 2'], width=bar_width, label=labels[1], color='blue')
    plt.bar(x + bar_width, merged_data['File 3'], width=bar_width, label=labels[2], color='darkblue')

    # Step 5: Customize the chart
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel(ylabel)
    plt.xticks(x, merged_data.index)  # Set x-axis labels to the dates (or group_by values) #, rotation=45
    
    ticks = plt.gca().get_xticks()
    labels = plt.gca().get_xticklabels()

    # Show every fourth label
    plt.xticks(ticks[::4], labels[::4], rotation=90) # Jan 2025: was commented out before.

    plt.legend()

    plt.tight_layout()  # Adjust layout to prevent label cutoff
    plt.savefig(output_file)

    # Step 6: Show the plot
    if show_plots:
        plt.show()

    plt.clf()


def cumulative_line_chart_cost_scroll(commit_file, revert_file, finalize_file, csv_row_names, show_plots,
                    group_by, gas_used, title, xlabel, format_x_axis, output_file):
    # Step 1: Load the CSV file into a pandas DataFrame
    df_commit = pd.read_csv(commit_file, header=None, names=csv_row_names)
    df_revert = pd.read_csv(revert_file, header=None, names=csv_row_names)
    df_finalize = pd.read_csv(finalize_file, header=None, names=csv_row_names)

    # Step 2: Group by 'block_num' and sum the 'gas_used'
    gas_per_block_commit = df_commit.groupby(group_by)[gas_used].sum().reset_index()
    gas_per_block_revert = df_revert.groupby(group_by)[gas_used].sum().reset_index()
    gas_per_block_finalize = df_finalize.groupby(group_by)[gas_used].sum().reset_index()

    # Step 3: Merge the datasets on 'block_num'
    merged_data = pd.merge(gas_per_block_commit, gas_per_block_revert, on=group_by, how='outer', suffixes=(' (Commit)', ' (Revert)')).fillna(0)
    merged_data = pd.merge(merged_data, gas_per_block_finalize, on=group_by, how='outer').fillna(0)
    merged_data.rename(columns={gas_used: 'Gas Used (Finalize)'}, inplace=True)

    # Step 4: Calculate the total gas used
    merged_data['Gas Used (Total)'] = (merged_data['Gas Used (Commit)'] + 
                                       merged_data['Gas Used (Revert)'] + 
                                       merged_data['Gas Used (Finalize)']) 

    # Step 5: Calculate cumulative sum for each gas used column
    merged_data['Cumulative Gas Used (Commit)'] = merged_data['Gas Used (Commit)'].cumsum()
    merged_data['Cumulative Gas Used (Revert)'] = merged_data['Gas Used (Revert)'].cumsum()
    merged_data['Cumulative Gas Used (Finalize)'] = merged_data['Gas Used (Finalize)'].cumsum()
    merged_data['Cumulative Gas Used (Total)'] = merged_data['Gas Used (Total)'].cumsum()

    # Step 6: Plot the cumulative data as a line chart
    plt.figure(figsize=(12, 8))  # Increase figure size (width=12, height=8)
    plt.plot(merged_data[group_by], merged_data['Cumulative Gas Used (Commit)'], label="Commit", color='skyblue')
    plt.plot(merged_data[group_by], merged_data['Cumulative Gas Used (Revert)'], label="Revert", color='orange')
    plt.plot(merged_data[group_by], merged_data['Cumulative Gas Used (Finalize)'], label="Finalize", color='green')
    plt.plot(merged_data[group_by], merged_data['Cumulative Gas Used (Total)'], label="All", color='black')

    # Step 7: Set custom x-axis ticks (real block numbers)
    plt.xticks(gas_per_block_commit[group_by]) # January 2025 change -- may need to change

    # Step 8: Customize the plot
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel('Cumulative Gas Used')

    if format_x_axis:
        ax = plt.gca()  # Get current axis
        ax.xaxis.set_major_formatter(mticker.StrMethodFormatter('{x:.0f}'))  # Format x-axis as integer

    ticks = plt.gca().get_xticks()
    labels = plt.gca().get_xticklabels()

    # Show every fourth label
    plt.xticks(ticks[::8], labels[::8], rotation=90)

    plt.legend()
    plt.grid(True)
    plt.tight_layout()  # Adjust layout to prevent label cutoff
    plt.savefig(output_file)

    # Step 9: Show the plot
    if show_plots:
        plt.show()

    plt.clf()

# 13 January 2025
def combined_cumulative_line_chart(
        propose_file, prove_file, verify_file, contest_file, 
        commit_file, revert_file, finalize_file, 
        csv_row_names, show_plots, group_by, gas_used, 
        title, xlabel, format_x_axis, output_file):
    # Load the CSV files into pandas DataFrames
    df_propose = pd.read_csv(propose_file, header=None, names=csv_row_names)
    df_prove = pd.read_csv(prove_file, header=None, names=csv_row_names)
    df_verify = pd.read_csv(verify_file, header=None, names=csv_row_names)
    df_contest = pd.read_csv(contest_file, header=None, names=csv_row_names)
    df_commit = pd.read_csv(commit_file, header=None, names=csv_row_names)
    df_revert = pd.read_csv(revert_file, header=None, names=csv_row_names)
    df_finalize = pd.read_csv(finalize_file, header=None, names=csv_row_names)

    # Group by 'block_num' and sum 'gas_used'
    gas_per_block_propose = df_propose.groupby(group_by)[gas_used].sum().reset_index()
    gas_per_block_prove = df_prove.groupby(group_by)[gas_used].sum().reset_index()
    gas_per_block_verify = df_verify.groupby(group_by)[gas_used].sum().reset_index()
    gas_per_block_contest = df_contest.groupby(group_by)[gas_used].sum().reset_index()
    gas_per_block_commit = df_commit.groupby(group_by)[gas_used].sum().reset_index()
    gas_per_block_revert = df_revert.groupby(group_by)[gas_used].sum().reset_index()
    gas_per_block_finalize = df_finalize.groupby(group_by)[gas_used].sum().reset_index()

    # Calculate cumulative sums
    gas_per_block_propose['Cumulative'] = gas_per_block_propose[gas_used].cumsum()
    gas_per_block_prove['Cumulative'] = gas_per_block_prove[gas_used].cumsum()
    gas_per_block_verify['Cumulative'] = gas_per_block_verify[gas_used].cumsum()
    gas_per_block_contest['Cumulative'] = gas_per_block_contest[gas_used].cumsum()
    gas_per_block_commit['Cumulative'] = gas_per_block_commit[gas_used].cumsum()
    gas_per_block_revert['Cumulative'] = gas_per_block_revert[gas_used].cumsum()
    gas_per_block_finalize['Cumulative'] = gas_per_block_finalize[gas_used].cumsum()

    # Plot cumulative data
    plt.figure(figsize=(12, 8))  # Increase figure size (width=12, height=8)
    plt.plot(gas_per_block_propose[group_by], gas_per_block_propose['Cumulative'], label="Cumulative Gas (Propose)", color='skyblue')
    plt.plot(gas_per_block_prove[group_by], gas_per_block_prove['Cumulative'], label="Cumulative Gas (Prove)", color='orange')
    plt.plot(gas_per_block_verify[group_by], gas_per_block_verify['Cumulative'], label="Cumulative Gas (Verify)", color='green')
    plt.plot(gas_per_block_contest[group_by], gas_per_block_contest['Cumulative'], label="Cumulative Gas (Contest)", color='red')
    plt.plot(gas_per_block_commit[group_by], gas_per_block_commit['Cumulative'], label="Cumulative Gas (Commit)", color='purple')
    plt.plot(gas_per_block_revert[group_by], gas_per_block_revert['Cumulative'], label="Cumulative Gas (Revert)", color='brown')
    plt.plot(gas_per_block_finalize[group_by], gas_per_block_finalize['Cumulative'], label="Cumulative Gas (Finalize)", color='black')

    # Customize the plot
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel('Cumulative Gas Used')

    if format_x_axis:
        ax = plt.gca()
        ax.xaxis.set_major_formatter(mticker.StrMethodFormatter('{x:.0f}'))

    ticks = plt.gca().get_xticks()
    labels = plt.gca().get_xticklabels()

    # Show every fourth label
    plt.xticks(ticks[::4], labels[::4], rotation=90)

    plt.legend()
    plt.grid(True)
    plt.tight_layout()  # Adjust layout to prevent label cutoff
    plt.savefig(output_file)

    # Show the plot
    if show_plots:
        plt.show()

    plt.clf()

def num_events_emitted_grouped(files, labels, output_file, show_plots, csv_row_names):
    # Step 1: Load the CSV files
    csv1 = pd.read_csv(files[0], header=None, names=csv_row_names)
    csv2 = pd.read_csv(files[1], header=None, names=csv_row_names)
    csv3 = pd.read_csv(files[2], header=None, names=csv_row_names)
    csv4 = pd.read_csv(files[3], header=None, names=csv_row_names)
    csv5 = pd.read_csv(files[4], header=None, names=csv_row_names)
    csv6 = pd.read_csv(files[5], header=None, names=csv_row_names)
    csv7 = pd.read_csv(files[6], header=None, names=csv_row_names)

    # Step 2: Count the number of rows (entries) in each CSV
    count1 = len(csv1)
    count2 = len(csv2)
    count3 = len(csv3)
    count4 = len(csv4)
    count5 = len(csv5)
    count6 = len(csv6)
    count7 = len(csv7)

    # Step 3: Create data for grouped bar chart
    counts_dataset1 = [count1, count2, count3, count4]  # Group 1 (Taiko)
    counts_dataset2 = [count5, count6, count7]  # Group 2 (Scroll)

    labels_dataset1 = [labels[0], labels[1], labels[2], labels[3]]  # Labels for group 1 (Taiko)
    labels_dataset2 = [labels[4], labels[5], labels[6]]  # Labels for group 2 (Scroll)

    # Define positions for the bars
    x1 = np.arange(len(labels_dataset1))  # Positions for dataset 1
    x2 = np.arange(len(labels_dataset2)) + len(labels_dataset1) + 1  # Offset positions for dataset 2

    # Step 4: Plot the bar chart
    plt.figure(figsize=(10, 6))

    # Plot bars for dataset 1
    bars1 = plt.bar(x1, counts_dataset1, width=0.9, label='Taiko', color='skyblue')

    # Plot bars for dataset 2
    bars2 = plt.bar(x2, counts_dataset2, width=0.9, label='Scroll', color='orange')

    # Add labels to the bars
    for bar in bars1:
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), str(bar.get_height()),
                 ha='center', va='bottom', fontsize=10)

    for bar in bars2:
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), str(bar.get_height()),
                 ha='center', va='bottom', fontsize=10)

    # Step 5: Customize the chart
    all_labels = labels_dataset1 + labels_dataset2
    plt.xticks(np.concatenate([x1, x2]), all_labels, rotation=45, ha='right')  # Rotate labels by 45 degrees

    plt.title('Number of Events Emitted')
    plt.xlabel('Event')
    plt.ylabel('Number of Emissions')
    plt.legend()

    # Step 6: Show the plot
    plt.tight_layout()
    plt.savefig(output_file)

    if show_plots:
        plt.show()

    plt.clf()


####
def combined_cumulative_costs_chart_man(propose_file, prove_file, verify_file, contest_file, commit_file, revert_file, finalize_file,
                                    csv_row_names, show_plots, group_by, gas_used, title, xlabel, format_x_axis, output_file):
    ### ---------------- TAIKO
    # Step 1: Load the CSV file into a pandas DataFrame
    df = pd.read_csv(propose_file, header=None, names=csv_row_names)
    df_prove = pd.read_csv(prove_file, header=None, names=csv_row_names)
    df_verify = pd.read_csv(verify_file, header=None, names=csv_row_names)
    df_contest = pd.read_csv(contest_file, header=None, names=csv_row_names)

    # Step 2: Group by 'block_num' and sum the 'gas_used'
    gas_per_block_propose = df.groupby(group_by)[gas_used].sum().reset_index()
    gas_per_block_prove = df_prove.groupby(group_by)[gas_used].sum().reset_index()
    gas_per_block_verify = df_verify.groupby(group_by)[gas_used].sum().reset_index()
    gas_per_block_contest = df_contest.groupby(group_by)[gas_used].sum().reset_index()

    # Step 3: Merge the datasets on 'block_num'
    merged_data = pd.merge(gas_per_block_propose, gas_per_block_prove, on=group_by, how='outer', suffixes=(' (Propose)', ' (Prove)')).fillna(0)
    merged_data = pd.merge(merged_data, gas_per_block_verify, on=group_by, how='outer').fillna(0)
    merged_data.rename(columns={gas_used: 'Gas Used (Verify)'}, inplace=True)
    merged_data = pd.merge(merged_data, gas_per_block_contest, on=group_by, how='outer').fillna(0)
    merged_data.rename(columns={gas_used: 'Gas Used (Contest)'}, inplace=True)

    # Step 4: Calculate the total gas used
    merged_data['Gas Used (Total)'] = (merged_data['Gas Used (Propose)'] + 
                                       merged_data['Gas Used (Prove)'] + 
                                       merged_data['Gas Used (Verify)'] + 
                                       merged_data['Gas Used (Contest)'])

    # Step 5: Calculate cumulative sum for each gas used column
    merged_data['Cumulative Gas Used (Propose)'] = merged_data['Gas Used (Propose)'].cumsum()
    merged_data['Cumulative Gas Used (Prove)'] = merged_data['Gas Used (Prove)'].cumsum()
    merged_data['Cumulative Gas Used (Contest)'] = merged_data['Gas Used (Contest)'].cumsum()
    merged_data['Cumulative Gas Used (Verify)'] = merged_data['Gas Used (Verify)'].cumsum()
    merged_data['Cumulative Gas Used (Total)'] = merged_data['Gas Used (Total)'].cumsum()

    # Step 6: Plot the cumulative data as a line chart
    #plt.plot(merged_data[group_by], merged_data['Cumulative Gas Used (Propose)'], label="Cumulative Gas Used (Propose)", color='skyblue')
    #plt.plot(merged_data[group_by], merged_data['Cumulative Gas Used (Prove)'], label="Cumulative Gas Used (Prove)", color='orange')
    #plt.plot(merged_data[group_by], merged_data['Cumulative Gas Used (Contest)'], label="Cumulative Gas Used (Contest)", color='red')
    #plt.plot(merged_data[group_by], merged_data['Cumulative Gas Used (Verify)'], label="Cumulative Gas Used (Verify)", color='green')
    #plt.plot(merged_data[group_by], merged_data['Cumulative Gas Used (Total)'], label="Cumulative Gas Used (All)", color='black')


    ### ---------------- SCROLLL
    # Step 1: Load the CSV file into a pandas DataFrame
    df_commit = pd.read_csv(commit_file, header=None, names=csv_row_names)
    df_revert = pd.read_csv(revert_file, header=None, names=csv_row_names)
    df_finalize = pd.read_csv(finalize_file, header=None, names=csv_row_names)

    # Step 2: Group by 'block_num' and sum the 'gas_used'
    gas_per_block_commit = df_commit.groupby(group_by)[gas_used].sum().reset_index()
    gas_per_block_revert = df_revert.groupby(group_by)[gas_used].sum().reset_index()
    gas_per_block_finalize = df_finalize.groupby(group_by)[gas_used].sum().reset_index()

    # Step 3: Merge the datasets on 'block_num'
    merged_dataS = pd.merge(gas_per_block_commit, gas_per_block_revert, on=group_by, how='outer', suffixes=(' (Commit)', ' (Revert)')).fillna(0)
    merged_dataS = pd.merge(merged_dataS, gas_per_block_finalize, on=group_by, how='outer').fillna(0)
    merged_dataS.rename(columns={gas_used: 'Gas Used (Finalize)'}, inplace=True)

    # Step 4: Calculate the total gas used
    merged_dataS['Gas Used (Total)'] = (merged_dataS['Gas Used (Commit)'] + 
                                       merged_dataS['Gas Used (Revert)'] + 
                                       merged_dataS['Gas Used (Finalize)']) 

    # Step 5: Calculate cumulative sum for each gas used column
    merged_dataS['Cumulative Gas Used (Commit)'] = merged_dataS['Gas Used (Commit)'].cumsum()
    merged_dataS['Cumulative Gas Used (Revert)'] = merged_dataS['Gas Used (Revert)'].cumsum()
    merged_dataS['Cumulative Gas Used (Finalize)'] = merged_dataS['Gas Used (Finalize)'].cumsum()
    merged_dataS['Cumulative Gas Used (Total)'] = merged_dataS['Gas Used (Total)'].cumsum()

    # Step 6: Plot the cumulative data as a line chart
    #plt.plot(merged_data[group_by], merged_data['Cumulative Gas Used (Commit)'], label="Cumulative Gas Used (Commit)", color='skyblue')
    #plt.plot(merged_data[group_by], merged_data['Cumulative Gas Used (Revert)'], label="Cumulative Gas Used (Revert)", color='orange')
    #plt.plot(merged_data[group_by], merged_data['Cumulative Gas Used (Finalize)'], label="Cumulative Gas Used (Finalize)", color='green')
    
    # For reference, colors from bar chart. Do not uncomment -- absolutely no need here.
    #bars1 = plt.bar(x1, counts_dataset1, width=0.9, label='Taiko', color='skyblue')
    #bars2 = plt.bar(x2, counts_dataset2, width=0.9, label='Scroll', color='orange')
    plt.figure(figsize=(12, 8))  # Increase figure size (width=12, height=8)

    plt.plot(merged_dataS[group_by], merged_dataS['Cumulative Gas Used (Total)'], label="Scroll", color='orange')
    plt.plot(merged_data[group_by], merged_data['Cumulative Gas Used (Total)'], label="Taiko", color='skyblue')

    # Step 7: Set custom x-axis ticks (real block numbers)
    plt.xticks(gas_per_block_commit[group_by]) 

    # Step 8: Customize the plot
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel('Cumulative Gas Used')

    if format_x_axis:
        ax = plt.gca()  # Get current axis
        ax.xaxis.set_major_formatter(mticker.StrMethodFormatter('{x:.0f}'))  # Format x-axis as integer

    ticks = plt.gca().get_xticks()
    labels = plt.gca().get_xticklabels()

    # Show every fourth label
    plt.xticks(ticks[::8], labels[::8], rotation=90)

    plt.legend()
    plt.grid(True)
    plt.tight_layout()  # Adjust layout to prevent label cutoff
    plt.savefig(output_file)

    # Step 9: Show the plot
    if show_plots:
        plt.show()

    plt.clf()

###
def clustered_scatter_plot(data_files, show_plots, output_file, csv_row_names, group_by, data, title, distinct, ylabel, labels):
    import pandas as pd
    import matplotlib.pyplot as plt
    import numpy as np

    # Step 1: Load the CSV files into pandas DataFrames
    df1 = pd.read_csv(data_files[0], header=None, names=csv_row_names)
    df2 = pd.read_csv(data_files[1], header=None, names=csv_row_names)
    df3 = pd.read_csv(data_files[2], header=None, names=csv_row_names)

    # Step 2: Group by 'group_by' and count the distinct EOAs per group
    if distinct:
        data_per_day_1 = df1.groupby(group_by)[data].nunique()
        data_per_day_2 = df2.groupby(group_by)[data].nunique()
        data_per_day_3 = df3.groupby(group_by)[data].nunique()
    else:
        data_per_day_1 = df1.groupby(group_by)[data].count()
        data_per_day_2 = df2.groupby(group_by)[data].count()
        data_per_day_3 = df3.groupby(group_by)[data].count()

    # Step 3: Merge the datasets on 'group_by' to ensure alignment
    merged_data = pd.DataFrame({
        'File 1': data_per_day_1,
        'File 2': data_per_day_2,
        'File 3': data_per_day_3
    }).fillna(0)  # Fill missing values with 0 if any

    # Convert index to datetime format and extract only MM-DD
    merged_data.index = pd.to_datetime(merged_data.index).strftime('%m-%d')

    # Step 3.1: Calculate and print the average height of each cluster (i.e., average of each dataset)
    avg_file_1 = merged_data['File 1'].mean()
    avg_file_2 = merged_data['File 2'].mean()
    avg_file_3 = merged_data['File 3'].mean()

    max_file_1 = merged_data['File 1'].max()
    max_file_2 = merged_data['File 2'].max()
    max_file_3 = merged_data['File 3'].max()

    print("Max value of " + data_files[0] + " points:", max_file_1)
    print("Max value of " + data_files[1] + " points:", max_file_2)
    print("Max value of " + data_files[2] + " points:", max_file_3)

    print("Average value of " + data_files[0] + " points:", avg_file_1)
    print("Average value of " + data_files[1] + " points:", avg_file_2)
    print("Average value of " + data_files[2] + " points:", avg_file_3)

    # Step 4: Plot the scatter plot
    plt.figure(figsize=(10, 6))
    
    # Determine the x locations for the groups
    x = np.arange(len(merged_data.index))

    # Plot the scatter points for each dataset
    # Plot the scatter points for each dataset with different symbols
    plt.scatter(x - 0.2, merged_data['File 1'], label=labels[0], color='red', marker='o')  # Circle
    plt.scatter(x, merged_data['File 2'], label=labels[1], color='blue', marker='s')           # Square
    plt.scatter(x + 0.2, merged_data['File 3'], label=labels[2], color='green', marker='^') # Triangle

    # Step 5: Customize the chart
    plt.title(title)
    plt.xlabel('2024 Date (MM-DD)')
    plt.ylabel(ylabel)
    plt.xticks(x, merged_data.index, rotation=90)  # Set x-axis labels to the dates (or group_by values)

    ticks = plt.gca().get_xticks()
    labels = plt.gca().get_xticklabels()

    # Show every fourth label
    plt.xticks(ticks[::4], labels[::4], rotation=90)  # Adjust for readability

    plt.legend()

    plt.tight_layout()  # Adjust layout to prevent label cutoff
    plt.savefig(output_file)

    # Step 6: Show the plot
    if show_plots:
        plt.show()

    plt.clf()


def line_chart_cost_scroll(commit_file, revert_file, finalize_file, csv_row_names, show_plots, 
                    group_by, gas_used, title, xlabel, format_x_axis, output_file):

    # Step 1: Load the CSV file into a pandas DataFrame
    df_commit = pd.read_csv(commit_file, header=None, names=csv_row_names)
    df_revert = pd.read_csv(revert_file, header=None, names=csv_row_names)
    df_finalize = pd.read_csv(finalize_file, header=None, names=csv_row_names)

    # Step 2: Group by 'group_by' (assumed to be a date column) and sum the 'gas_used'
    gas_per_block_commit = df_commit.groupby(group_by)[gas_used].sum().reset_index()
    gas_per_block_revert = df_revert.groupby(group_by)[gas_used].sum().reset_index()
    gas_per_block_finalize = df_finalize.groupby(group_by)[gas_used].sum().reset_index()

    # Step 3: Merge the datasets on 'group_by' to ensure alignment
    merged_data = pd.merge(gas_per_block_commit, gas_per_block_revert, on=group_by, how='outer', suffixes=(' (Commit)', ' (Revert)')).fillna(0)
    merged_data = pd.merge(merged_data, gas_per_block_finalize, on=group_by, how='outer').fillna(0)
    merged_data.rename(columns={gas_used: 'Gas Used (Finalize)'}, inplace=True)

    # Convert the index column to datetime format and extract only MM-DD
    merged_data[group_by] = pd.to_datetime(merged_data[group_by]).dt.strftime('%m-%d')

    # Step 4: Calculate the total gas used
    merged_data['Gas Used (Total)'] = merged_data['Gas Used (Commit)'] + merged_data['Gas Used (Revert)'] + merged_data['Gas Used (Finalize)']

    # Step 5: Plot the data as a line graph
    plt.figure(figsize=(12, 8))
    plt.plot(merged_data[group_by], merged_data['Gas Used (Commit)'], label="Commit", color='skyblue')
    plt.plot(merged_data[group_by], merged_data['Gas Used (Revert)'], label="Revert", color='orange')
    plt.plot(merged_data[group_by], merged_data['Gas Used (Finalize)'], label="Finalize", color='red')
    plt.plot(merged_data[group_by], merged_data['Gas Used (Total)'], label="All", color='black')

    # Step 6: Customize the x-axis labels
    plt.xticks(rotation=90)
    plt.xlabel(xlabel)
    plt.ylabel('Total Gas Used')
    plt.title(title)

    if format_x_axis:
        ax = plt.gca()
        ax.xaxis.set_major_formatter(mticker.StrMethodFormatter('{x:.0f}'))

    # Show every eighth label for better readability
    ticks = plt.gca().get_xticks()
    labels = plt.gca().get_xticklabels()
    plt.xticks(ticks[::8], labels[::8], rotation=90)

    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_file)

    # Step 7: Show the plot if required
    if show_plots:
        plt.show()

    plt.clf()

def line_chart_cost(propose_file, prove_file, verify_file, contest_file, csv_row_names, show_plots, 
                    group_by, gas_used, title, xlabel, format_x_axis, output_file):
    
    # Step 1: Load the CSV file into pandas DataFrames
    df_propose = pd.read_csv(propose_file, header=None, names=csv_row_names)
    df_prove = pd.read_csv(prove_file, header=None, names=csv_row_names)
    df_verify = pd.read_csv(verify_file, header=None, names=csv_row_names)
    df_contest = pd.read_csv(contest_file, header=None, names=csv_row_names)

    # Step 2: Group by 'group_by' (assumed to be a date column) and sum 'gas_used'
    gas_per_block_propose = df_propose.groupby(group_by)[gas_used].sum().reset_index()
    gas_per_block_prove = df_prove.groupby(group_by)[gas_used].sum().reset_index()
    gas_per_block_verify = df_verify.groupby(group_by)[gas_used].sum().reset_index()
    gas_per_block_contest = df_contest.groupby(group_by)[gas_used].sum().reset_index()

    # Step 3: Merge datasets on 'group_by' to ensure alignment
    merged_data = pd.merge(gas_per_block_propose, gas_per_block_prove, on=group_by, how='outer', suffixes=(' (Propose)', ' (Prove)')).fillna(0)
    merged_data = pd.merge(merged_data, gas_per_block_verify, on=group_by, how='outer').fillna(0)
    merged_data.rename(columns={gas_used: 'Gas Used (Verify)'}, inplace=True)
    merged_data = pd.merge(merged_data, gas_per_block_contest, on=group_by, how='outer').fillna(0)
    merged_data.rename(columns={gas_used: 'Gas Used (Contest)'}, inplace=True)

    # Convert 'group_by' column to datetime format and extract only MM-DD
    merged_data[group_by] = pd.to_datetime(merged_data[group_by]).dt.strftime('%m-%d')

    # Step 4: Calculate the total gas used
    merged_data['Gas Used (Total)'] = (
        merged_data['Gas Used (Propose)'] + 
        merged_data['Gas Used (Prove)'] + 
        merged_data['Gas Used (Verify)'] + 
        merged_data['Gas Used (Contest)']
    )

    # Step 5: Plot the data as a line graph
    plt.figure(figsize=(12, 8))
    plt.plot(merged_data[group_by], merged_data['Gas Used (Propose)'], label="Propose", color='skyblue')
    plt.plot(merged_data[group_by], merged_data['Gas Used (Prove)'], label="Prove", color='orange')
    plt.plot(merged_data[group_by], merged_data['Gas Used (Contest)'], label="Contest", color='red')
    plt.plot(merged_data[group_by], merged_data['Gas Used (Verify)'], label="Verify", color='green')
    plt.plot(merged_data[group_by], merged_data['Gas Used (Total)'], label="All", color='black')

    # Step 6: Customize the x-axis labels
    plt.xticks(rotation=90)
    plt.xlabel(xlabel)
    plt.ylabel('Total Gas Used')
    plt.title(title)

    if format_x_axis:
        ax = plt.gca()
        ax.xaxis.set_major_formatter(mticker.StrMethodFormatter('{x:.0f}'))

    # Show every eighth label for better readability
    ticks = plt.gca().get_xticks()
    labels = plt.gca().get_xticklabels()
    plt.xticks(ticks[::8], labels[::8], rotation=90)

    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_file)

    # Step 7: Show the plot if required
    if show_plots:
        plt.show()

    plt.clf()

def combined_cumulative_costs_chart_man_all(propose_file, prove_file, verify_file, contest_file, commit_file, revert_file, finalize_file,
                                    csv_row_names, show_plots, group_by, gas_used, title, xlabel, format_x_axis, output_file):
    
    plt.figure(figsize=(12, 8))  # Increase figure size (width=12, height=8)

    ### ---------------- TAIKO
    # Step 1: Load the CSV file into pandas DataFrames
    df_propose = pd.read_csv(propose_file, header=None, names=csv_row_names)
    df_prove = pd.read_csv(prove_file, header=None, names=csv_row_names)
    df_verify = pd.read_csv(verify_file, header=None, names=csv_row_names)
    df_contest = pd.read_csv(contest_file, header=None, names=csv_row_names)

    # Step 2: Group by 'group_by' (assumed to be a date column) and sum 'gas_used'
    gas_per_block_propose = df_propose.groupby(group_by)[gas_used].sum().reset_index()
    gas_per_block_prove = df_prove.groupby(group_by)[gas_used].sum().reset_index()
    gas_per_block_verify = df_verify.groupby(group_by)[gas_used].sum().reset_index()
    gas_per_block_contest = df_contest.groupby(group_by)[gas_used].sum().reset_index()

    # Step 3: Merge datasets on 'group_by' to ensure alignment
    merged_data = pd.merge(gas_per_block_propose, gas_per_block_prove, on=group_by, how='outer', suffixes=(' (Propose)', ' (Prove)')).fillna(0)
    merged_data = pd.merge(merged_data, gas_per_block_verify, on=group_by, how='outer').fillna(0)
    merged_data.rename(columns={gas_used: 'Gas Used (Verify)'}, inplace=True)
    merged_data = pd.merge(merged_data, gas_per_block_contest, on=group_by, how='outer').fillna(0)
    merged_data.rename(columns={gas_used: 'Gas Used (Contest)'}, inplace=True)

    # Convert 'group_by' column to datetime format and extract only MM-DD
    merged_data[group_by] = pd.to_datetime(merged_data[group_by]).dt.strftime('%m-%d')

    # Step 4: Calculate the total gas used
    merged_data['Gas Used (Total)'] = (
        merged_data['Gas Used (Propose)'] + 
        merged_data['Gas Used (Prove)'] + 
        merged_data['Gas Used (Verify)'] + 
        merged_data['Gas Used (Contest)']
    )

    # Step 5: Calculate cumulative sum for each gas used column
    cumulative_columns = ['Propose', 'Prove', 'Contest', 'Verify', 'Total']
    for col in cumulative_columns:
        merged_data[f'Cumulative Gas Used ({col})'] = merged_data[f'Gas Used ({col})'].cumsum()

    ### ---------------- SCROLL
    # Step 1: Load the CSV file into pandas DataFrames
    df_commit = pd.read_csv(commit_file, header=None, names=csv_row_names)
    df_revert = pd.read_csv(revert_file, header=None, names=csv_row_names)
    df_finalize = pd.read_csv(finalize_file, header=None, names=csv_row_names)

    # Step 2: Group by 'group_by' and sum the 'gas_used'
    gas_per_block_commit = df_commit.groupby(group_by)[gas_used].sum().reset_index()
    gas_per_block_revert = df_revert.groupby(group_by)[gas_used].sum().reset_index()
    gas_per_block_finalize = df_finalize.groupby(group_by)[gas_used].sum().reset_index()

    # Step 3: Merge datasets on 'group_by'
    merged_dataS = pd.merge(gas_per_block_commit, gas_per_block_revert, on=group_by, how='outer', suffixes=(' (Commit)', ' (Revert)')).fillna(0)
    merged_dataS = pd.merge(merged_dataS, gas_per_block_finalize, on=group_by, how='outer').fillna(0)
    merged_dataS.rename(columns={gas_used: 'Gas Used (Finalize)'}, inplace=True)

    # Convert 'group_by' column to datetime format and extract only MM-DD
    merged_dataS[group_by] = pd.to_datetime(merged_dataS[group_by]).dt.strftime('%m-%d')

    # Step 4: Calculate the total gas used
    merged_dataS['Gas Used (Total)'] = (
        merged_dataS['Gas Used (Commit)'] + 
        merged_dataS['Gas Used (Revert)'] + 
        merged_dataS['Gas Used (Finalize)']
    )

    # Step 5: Calculate cumulative sum for each gas used column
    cumulative_columnsS = ['Commit', 'Revert', 'Finalize', 'Total']
    for col in cumulative_columnsS:
        merged_dataS[f'Cumulative Gas Used ({col})'] = merged_dataS[f'Gas Used ({col})'].cumsum()

    # Step 6: Plot the cumulative data as a line chart
    #plt.plot(merged_dataS[group_by], merged_dataS['Cumulative Gas Used (Commit)'], label="Scroll - Commit", color='brown', linestyle='--')
    #plt.plot(merged_dataS[group_by], merged_dataS['Cumulative Gas Used (Revert)'], label="Scroll - Revert", color='green', linestyle='--')
    #plt.plot(merged_dataS[group_by], merged_dataS['Cumulative Gas Used (Finalize)'], label="Scroll - Finalize", color='gray', linestyle='--')
    #plt.plot(merged_dataS[group_by], merged_dataS['Cumulative Gas Used (Total)'], label="Scroll - All", color='black')

    #plt.plot(merged_data[group_by], merged_data['Cumulative Gas Used (Total)'], label="Taiko - All", color='red')
    #plt.plot(merged_data[group_by], merged_data['Cumulative Gas Used (Propose)'], label="Taiko - Propose", color='burlywood', linestyle='-.')
    #plt.plot(merged_data[group_by], merged_data['Cumulative Gas Used (Prove)'], label="Taiko - Prove", color='darkslategray', linestyle='-.')
    #plt.plot(merged_data[group_by], merged_data['Cumulative Gas Used (Contest)'], label="Taiko - Contest", color='darkgreen', linestyle='-.')
    #plt.plot(merged_data[group_by], merged_data['Cumulative Gas Used (Verify)'], label="Taiko - Verify", color='blue', linestyle='-.')

    # Define a list of 9 distinct colors
    colors = ['#E6194B', '#3CB44B', '#FF8C00', '#008000', '#911EB4',
            '#46F0F0', '#F032E6', '#FFD700', '#8B4513']

    # Apply the colors to the plot lines
    plt.plot(merged_dataS[group_by], merged_dataS['Cumulative Gas Used (Commit)'], label="Scroll - Commit", color='red', linestyle='--')
    plt.plot(merged_dataS[group_by], merged_dataS['Cumulative Gas Used (Revert)'], label="Scroll - Revert", color='blue', linestyle='--')
    plt.plot(merged_dataS[group_by], merged_dataS['Cumulative Gas Used (Finalize)'], label="Scroll - Finalize", color=colors[2], linestyle='--')
    plt.plot(merged_dataS[group_by], merged_dataS['Cumulative Gas Used (Total)'], label="Scroll - All", color=colors[3])

    plt.plot(merged_data[group_by], merged_data['Cumulative Gas Used (Total)'], label="Taiko - All", color='black')
    plt.plot(merged_data[group_by], merged_data['Cumulative Gas Used (Propose)'], label="Taiko - Propose", color=colors[5], linestyle='-.')
    plt.plot(merged_data[group_by], merged_data['Cumulative Gas Used (Prove)'], label="Taiko - Prove", color=colors[6], linestyle='-.')
    plt.plot(merged_data[group_by], merged_data['Cumulative Gas Used (Contest)'], label="Taiko - Contest", color=colors[7], linestyle='-.')
    plt.plot(merged_data[group_by], merged_data['Cumulative Gas Used (Verify)'], label="Taiko - Verify", color=colors[8], linestyle='-.')


    # Step 7: Customize the x-axis labels
    plt.xticks(rotation=90)
    plt.xlabel(xlabel)
    plt.ylabel('Cumulative Gas Used')
    plt.title(title)

    if format_x_axis:
        ax = plt.gca()
        ax.xaxis.set_major_formatter(mticker.StrMethodFormatter('{x:.0f}'))

    # Show every eighth label for better readability
    ticks = plt.gca().get_xticks()
    labels = plt.gca().get_xticklabels()
    plt.xticks(ticks[::8], labels[::8], rotation=90)

    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_file)

    # Step 8: Show the plot if required
    if show_plots:
        plt.show()

    plt.clf()


def scatter_plot_distinct_per_block(data_file, show_plots, output_file, csv_row_names, group_by, data, title, distinct, ylabel):

    # Step 1: Load the CSV file into a pandas DataFrame
    df = pd.read_csv(data_file, header=None, names=csv_row_names)

    # Step 2: Group by the specified column
    if distinct:
        data_per_block = df.groupby(group_by)[data].nunique()
    else:
        data_per_block = df.groupby(group_by)[data].count()

    # Step 3: Extract x (group_by) and y (data values) for the scatter plot
    x = data_per_block.index  # Block numbers or group_by values
    y = data_per_block.values  # Distinct or count values

    # Count occurrences of each y-value
    unique_y, y_counts = np.unique(y, return_counts=True)

    # Step 4: Create the scatter plot
    plt.figure(figsize=(10, 6))
    plt.scatter(x, y, color='black', s=10, alpha=0.7, marker='^')  # `s` controls point size, `alpha` adds transparency

    # Step 5: Customize the chart
    plt.title(title)
    plt.xlabel('L1 Block')
    plt.ylabel(ylabel)
    plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(integer=True))  # Ensure y-axis values are integers

    # Step 6: Format x-axis labels as integers
    ax = plt.gca()  # Get the current axis
    ax.xaxis.set_major_formatter(ScalarFormatter())  # Use ScalarFormatter for the x-axis
    ax.ticklabel_format(style='plain', axis='x')  # Ensure plain formatting (no scientific notation)

    # Step 7: Annotate the count of each y-value slightly above and left of the rightmost points
    max_x = max(x)  # Get the maximum x value for annotation placement
    x_offset = (max_x - min(x)) * 0.05  # Shift labels slightly left (5% of range)
    y_offset = 0.05  # Small offset to move labels slightly above points
    REFERENCE_VALUE = 1362564  # The fixed reference for percentage calculation

    #for y_val, count in zip(unique_y, y_counts):
    #    plt.text(max_x - x_offset, y_val + y_offset, f"{count}", fontsize=10, verticalalignment='bottom', horizontalalignment='right', color='red')
    for y_val, count in zip(unique_y, y_counts):
        percent = (count / REFERENCE_VALUE) * 100  # Compute percentage
        label_text = f"{count} ({percent:.2f}%)"  # Format label with 2 decimal places

        plt.text(max_x - x_offset, y_val + y_offset, label_text, fontsize=10, 
                 verticalalignment='bottom', horizontalalignment='right', color='red')


    # Step 8: Adjust layout and save the plot
    plt.tight_layout()  # Adjust layout to prevent label cutoff
    plt.savefig(output_file)

    # Step 9: Show the plot if required
    if show_plots:
        plt.show()

    plt.clf()
