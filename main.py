import math
import csv
import scipy.stats as stats
import matplotlib.pyplot as plt

data = {}

min = float("inf")
max = float("-inf")

n = 0
sum = 0
sd_sum = 0

probabilities = {}
highest_prob = 0

if __name__ == "__main__":
    print("starting generation of statistics...")

    with open('data.csv', mode='r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            key, value = int(row[0]), int(row[1])
            data[key] = value

    print("Read data...")
    
    for k in data.keys():
        n += data[k]
        sum += k * data[k]

        if k < min:
            min = k

        if k > max:
            max = k

    mean = sum / n

    for k in data.keys():
        sd_sum += math.pow(k - mean, 2) * data[k]

    sd = math.sqrt(sd_sum / n)

    print("Mean", mean)
    print("Sd", sd)

    c = min

    while c <= max:
        za = c-1
        zb = c+1

        za = (za - mean) / sd
        zb = (zb - mean) / sd

        prob = (stats.norm.cdf(zb) - stats.norm.cdf(za)) * 100
        probabilities[c] = prob

        if prob > highest_prob:
            highest_prob = prob

        c += 1

    values = list(probabilities.keys())
    probs = list(probabilities.values())

    plt.figure(figsize=(10, 6))
    plt.plot(values, probs, marker="o")

    plt.xlabel("Cycle Length (days)")
    plt.ylabel("Probability in %")
    plt.title("Probability Distribution of Cycle Lengths")

    plt.grid(True)
    plt.text(mean, highest_prob - 3, f"mean={round(mean, 2)}")
    #plt.show()

    plt.savefig("./docs/images/graph.png")

    
