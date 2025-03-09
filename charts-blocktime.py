import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file
file_path_taiko = "time-data/13-Jan-2025-Taiko-block-intervals-clean.csv"  
output_file_taiko = "results-blocktime/Taiko-500-plot.png" 
title_taiko = "Taiko Average Block Time in 500-Block Intervals with Moving Average"
interval_ticks_taiko = 50

file_path_scroll = "time-data/13-Jan-2025-Scroll-block-intervals-500-infura.csv"  
output_file_scroll = "results-blocktime/Scroll-500-plot.png" 
title_scroll = "Scroll Average Block Time in 500-Block Intervals with Moving Average"
interval_ticks_scroll = 500

output_file_both = "results-blocktime/Both-500-plot.png" 
title_both = "Taiko and Scroll Average Block Time in 500-Block Intervals with Moving Average"
interval_ticks_both = 500
labels_both = ('Taiko', 'Scroll')


def make_plot(file_path, output_file, title, interval_ticks):
    print("Making plot titled", title)
    data = pd.read_csv(file_path)

    # Prepare the data for plotting
    interval_labels = data['end_block'].astype(str)  # Convert to string for categorical labels
    average_times = data['average_time']

    # Calculate the moving average (10 bars)
    window_size = 10
    moving_average = average_times.rolling(window=window_size).mean()

    # Create the bar chart
    plt.figure(figsize=(12, 8))  # Increase figure size (width=12, height=8)
    plt.bar(interval_labels, average_times, color='skyblue', label='Average Time')

    # Add the moving average line
    plt.plot(interval_labels, moving_average, color='red', linestyle='-', linewidth=2, label='10-Bar Moving Average')

    # Add labels and title
    plt.xlabel('End Block in 500-Block Interval')
    plt.ylabel('Average Time (s)')
    plt.title(title)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    plt.xticks(range(0, len(interval_labels), interval_ticks), interval_labels[::interval_ticks], rotation=45)

    # Add a legend
    plt.legend()

    # Save the plot to a file
    plt.tight_layout()
    plt.savefig(output_file, dpi=300)

    # Show the plot (optional)
    #plt.show()

    print(f"Bar chart with moving average saved to {output_file}")

def make_scatter_plot(file_path, output_file, title, interval_ticks):
    print("Making scatter plot titled", title)
    data = pd.read_csv(file_path)

    # Prepare the data for plotting
    interval_labels = data['end_block'].astype(str)  # Convert to string for categorical labels
    average_times = data['average_time']

    # Calculate the moving average (10 points)
    window_size = 10
    moving_average = average_times.rolling(window=window_size).mean()

    # Create the scatter plot
    plt.figure(figsize=(12, 8))  # Increase figure size (width=12, height=8)
    plt.scatter(interval_labels, average_times, color='skyblue', label='Average Time', alpha=0.7)

    # Add the moving average line
    plt.plot(interval_labels, moving_average, color='red', linestyle='-', linewidth=2, label='10-Point Moving Average')

    # Add labels and title
    plt.xlabel('End Block in 500-Block Interval')
    plt.ylabel('Average Time (s)')
    plt.title(title)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Customize x-axis ticks and labels
    plt.xticks(range(0, len(interval_labels), interval_ticks), interval_labels[::interval_ticks], rotation=45)

    # Add a legend
    plt.legend()

    # Save the plot to a file
    plt.tight_layout()
    plt.savefig(output_file, dpi=300)

    # Show the plot (optional)
    # plt.show()

    print(f"Scatter plot with moving average saved to {output_file}")


### does not work well because the data set doesn't have matching buckets.
def make_dual_scatter_plot(file_path1, file_path2, output_file, title, interval_ticks, labels):
    """
    Creates a scatter plot with two datasets on the same plot.

    Args:
        file_path1 (str): Path to the first CSV file.
        file_path2 (str): Path to the second CSV file.
        output_file (str): Path to save the output plot.
        title (str): Title of the plot.
        interval_ticks (int): Interval for x-axis tick labels.
        labels (tuple): Labels for the two datasets (e.g., ("Dataset 1", "Dataset 2")).
    """
    print(f"Making scatter plot titled '{title}' with two datasets")

    # Load datasets
    data1 = pd.read_csv(file_path1)
    data2 = pd.read_csv(file_path2)

    # Prepare the data for plotting
    interval_labels1 = data1['end_block'].astype(str)
    average_times1 = data1['average_time']
    interval_labels2 = data2['end_block'].astype(str)
    average_times2 = data2['average_time']

    # Calculate moving averages
    window_size = 10
    moving_average1 = average_times1.rolling(window=window_size).mean()
    moving_average2 = average_times2.rolling(window=window_size).mean()

    # Create the scatter plot
    plt.figure(figsize=(12, 8))

    # Dataset 1
    plt.scatter(interval_labels1, average_times1, color='skyblue', label=f'{labels[0]} - Average Time', alpha=0.7)
    plt.plot(interval_labels1, moving_average1, color='blue', linestyle='-', linewidth=2, label=f'{labels[0]} - Moving Average')

    # Dataset 2
    plt.scatter(interval_labels2, average_times2, color='lightcoral', label=f'{labels[1]} - Average Time', alpha=0.7)
    plt.plot(interval_labels2, moving_average2, color='red', linestyle='-', linewidth=2, label=f'{labels[1]} - Moving Average')

    # Add labels and title
    plt.xlabel('End Block in 500-Block Interval')
    plt.ylabel('Average Time (s)')
    plt.title(title)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Customize x-axis ticks and labels
    plt.xticks(range(0, max(len(interval_labels1), len(interval_labels2)), interval_ticks),
               interval_labels1[::interval_ticks] if len(interval_labels1) > len(interval_labels2) else interval_labels2[::interval_ticks],
               rotation=45)

    # Add a legend
    plt.legend()

    # Save the plot to a file
    plt.tight_layout()
    plt.savefig(output_file, dpi=300)

    # Show the plot (optional)
    # plt.show()

    print(f"Scatter plot with two datasets saved to {output_file}")


#make_plot(file_path_taiko, output_file_taiko, title_taiko, interval_ticks_taiko)
#make_plot(file_path_scroll, output_file_scroll, title_scroll, interval_ticks_scroll)
    
make_scatter_plot(file_path_taiko, output_file_taiko, title_taiko, interval_ticks_taiko)
make_scatter_plot(file_path_scroll, output_file_scroll, title_scroll, interval_ticks_scroll)
    
#make_dual_scatter_plot(file_path_taiko, file_path_scroll, output_file_both, title_both, interval_ticks_both, labels_both)
