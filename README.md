# statistics-simulations

The scenario simulated is the following.

One new data point (positive decimal value) comes every day, for a total of 365 days of simulation.
The data points are distributed as a normal distribution, starting from a mean of 100 and a standard deviation of 25.
Every time a new data point X arrives, we do the following:
- we calculate the average M and the standard deviation S of the last 7 data points (i.e. last 7 days)
- we calculate the z-score Z of the new data point X as the absolute value of (X - M) / S
- if Z is below 2, we print "Bin 0"
- if Z is below 2.5, we print "Bin 1"
- if Z is above 2.5, we print "Bin 2"

We also report, after 365 days of simulation, the numbers of Bin 0, 1 and 2.
We then increase both the mean and the standard deviation by a percentage "drift", and run the entire algorithm with drift from 0 to 30%, in increments of 0.2%.
For each drift, we store the detection rate, calculated as (items in bin 1 + items in bin 2) divided by the sum of items in all the bins.
We get a dictionary of drifts (decimal numbers) to detection rates (also decimal numbers).
We finally draw a graph, with drifts on the x-axis and detection rates on the y-axis.