import numpy as np
import matplotlib.pyplot as plt
from collections import deque

# Initialize a deque with maxlen 7 to store the last 7 data points
data_points = deque(maxlen=7)

# Initialize counters for each bin
bin_counts = {"Bin 0": 0, "Bin 1": 0, "Bin 2": 0}

# Define the initial mean and standard deviation
initial_mean = 100
initial_standard_deviation = 25

# Simulate for drift percentages from 0 to 10% in increments of 0.2%
drifts_to_detection_rates = {}
for drift in np.arange(0, 30.2, 0.2):
    print(f"Drift: {round(drift, 1)}%")
    
    # Reset the data points and bin counts for each drift percentage
    data_points.clear()
    bin_counts = {"Bin 0": 0, "Bin 1": 0, "Bin 2": 0}
        
    # Simulate for 365 days
    for day in range(1, 366):
        # Calculate the current mean
        current_mean = initial_mean * (1 + drift * day / 100)
        current_standard_deviation = initial_standard_deviation * (1 + drift * day / 100)

        # Generate a new data point from a normal distribution with the current mean
        X = np.random.normal(current_mean, current_standard_deviation)
        
        # Append the new data point to the deque
        data_points.append(X)
        
        # If there are less than 7 data points, continue to the next iteration
        if len(data_points) < 7:
            continue
        
        # Calculate the average (M) and standard deviation (S) of the last 7 data points
        M = np.mean(data_points)
        S = np.std(data_points)
        
        # Calculate the z-score (Z) of the new data point X
        Z = abs((X - M) / S)
        
        # Determine the bin number based on the z-score and increment the corresponding counter
        if Z < 2:
            bin_counts["Bin 0"] += 1
        elif Z < 2.5:
            bin_counts["Bin 1"] += 1
        else:
            bin_counts["Bin 2"] += 1
    
    # Print the counts for each bin
    for bin, count in bin_counts.items():
        print(f"{bin}: {count}")

    bin0_counts = bin_counts["Bin 0"]
    bin1_counts = bin_counts["Bin 1"]
    bin2_counts = bin_counts["Bin 2"]
    detection_rate = (bin1_counts + bin2_counts)/(bin0_counts + bin1_counts + bin2_counts) * 100
    print(f"Detection rate: {round(detection_rate)}%")
    drifts_to_detection_rates[drift] = detection_rate
    print()

# Create lists of x values (drifts) and y values (detection rates)
x_values = list(drifts_to_detection_rates.keys())
y_values = list(drifts_to_detection_rates.values())

# Create a figure and a set of subplots
fig, ax = plt.subplots()

# Plot x and y values
ax.plot(x_values, y_values)

# Set labels for x and y axis
ax.set_xlabel('Drifts (%)')
ax.set_ylabel('Detection Rates (%)')

# Set title for the plot
ax.set_title('Drifts vs Detection Rates')

# Display the plot
plt.show()