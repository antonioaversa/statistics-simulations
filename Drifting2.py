import numpy as np
import matplotlib.pyplot as plt
from collections import deque

def top(window=30, gaussian=True, firstBin=2.0, secondBin=2.5):

    def simulate(drift, days=365, mean=100, std_dev=10):
        # Initialize bins
        bins = [0, 0, 0]

        # Initialize deque with maxlen equal to window size
        last_days = deque(maxlen=window)

        # Generate data points
        data_points = np.random.normal(mean, std_dev, days)

        for day, X in enumerate(data_points, start=1):
            # Adjust mean and std_dev for drift
            adjusted_mean = mean * (1 + drift * day)
            adjusted_std_dev = std_dev * (1 + drift * day)

            if (gaussian):
                # Generate new data point with adjusted mean and std_dev
                X = np.random.normal(adjusted_mean, adjusted_std_dev, 1)[0]
            else:
                # Here, 'df' is the degrees of freedom parameter. Lower values give heavier tails.
                df = 1
                X = np.random.standard_t(df, 1)[0] * adjusted_std_dev + adjusted_mean

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

    # Get drifts and detection rates as lists
    drifts = list(drifts_to_detection_rates.keys())
    detection_rates = list(drifts_to_detection_rates.values())

    # Plot drifts vs detection rates
    plt.scatter(drifts, detection_rates)

    # Calculate coefficients for the polynomial (Here, 1 means we want a degree one polynomial which is a straight line)
    coefficients = np.polyfit(drifts, detection_rates, 1)

    # Generate y-values based on the trend line
    trendline = np.poly1d(coefficients)
    plt.plot(drifts, trendline(drifts), color='red')

    plt.xlabel('Drifts')
    plt.ylabel('Detection Rates')
    plt.title('Drifts vs Detection Rates')
    plt.show(block=True)

top(window=7, gaussian=True, firstBin=2.0, secondBin=2.5)
top(window=14, gaussian=True, firstBin=2.0, secondBin=2.5)
top(window=30, gaussian=True, firstBin=2.0, secondBin=2.5)
top(window=7, gaussian=False, firstBin=2.0, secondBin=2.5)
top(window=14, gaussian=False, firstBin=2.0, secondBin=2.5)
top(window=30, gaussian=False, firstBin=2.0, secondBin=2.5)

plt.show()