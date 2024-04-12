import numpy as np
import matplotlib.pyplot as plt
from collections import deque

def simulate(drift, days=365, window=7, mean=100, std_dev=25):
    # Initialize bins
    bins = [0, 0, 0]

    # Initialize deque with maxlen equal to window size
    last_days = deque(maxlen=window)

    # Generate data points
    data_points = np.random.normal(mean, std_dev, days)

    for day, X in enumerate(data_points, start=1):
        # Adjust mean and std_dev for drift
        adjusted_mean = mean + mean * (drift * day / 100)
        adjusted_std_dev = std_dev + std_dev * (drift * day / 100)

        # Generate new data point with adjusted mean and std_dev
        X = np.random.normal(adjusted_mean, adjusted_std_dev, 1)[0]

        # Append new data point to last_days
        last_days.append(X)

        # Calculate mean and std_dev of last_days
        M = np.mean(last_days)
        S = np.std(last_days)

        # Calculate z-score
        Z = abs((X - M) / S)

        # Update bins
        if Z < 2:
            bins[0] += 1
        elif Z < 2.5:
            bins[1] += 1
        else:
            bins[2] += 1

    # Calculate detection rate
    detection_rate = (bins[1] + bins[2]) / sum(bins)

    return detection_rate

# Initialize dictionary for drifts to detection rates
drifts_to_detection_rates = {}

# Run simulation for drifts from 0 to 30% in increments of 0.2%
for drift in np.arange(0, 0.3, 0.002):
    drifts_to_detection_rates[drift] = simulate(drift)

# Plot drifts vs detection rates
plt.plot(list(drifts_to_detection_rates.keys()), list(drifts_to_detection_rates.values()))
plt.xlabel('Drifts')
plt.ylabel('Detection Rates')
plt.title('Drifts vs Detection Rates')
plt.show()