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

if __name__ == "__main__":
    print("starting generation of statistics...")

    with open('data.csv', mode='r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            key, value = int(row[0]), int(row[1])
            data[key] = value
    
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

        c += 1

    values = list(probabilities.keys())
    probs = list(probabilities.values())

    max_prob = float("-inf")
    min_prob = float("inf")

    for p in probs:
        print(p)
        if p > max_prob:
            max_prob = round(p)

        if p < min_prob:
            min_prob = round(p)

    fig, ax = plt.subplots()
    fig.set_size_inches(16, 10)

    ax.set_title('Distribution of Cycle Length Probabilities')
    ax.plot(values, probs, marker='o', linestyle='-', color='b')
    ax.set_xlabel('Cycle Length (Days)')
    ax.set_ylabel('Probabilities in %')

    x = list(range(min, max+1))
    y = list(range(min_prob, max_prob+1))

    ax.set_xticks(x)
    ax.set_xticklabels([str(i) for i in x])

    ax.set_yticks(y)
    ax.set_yticklabels([str(round(i, 2)) for i in y])

    ax.annotate(f'Mean: {mean:.2f}', xy=(mean, max_prob), xytext=(mean - 5, max_prob - 5),
                arrowprops=dict(facecolor='black', arrowstyle='->'))

    ax.grid(True)

    plt.savefig("./docs/images/graph.png")

    # Probs table
    table_data = []
    for val, prob in zip(values, probs):
        table_data.append([val, f'{prob:.2f}%'])

    fig2, ax2 = plt.subplots(figsize=(20, 12))
    fig2.set_size_inches(20, 24)

    ax2.axis('off')  # Turn off axis for the table plot
    table_plot = ax2.table(cellText=table_data, colLabels=["Cycle Length (Days)", "Probability in %"], loc='center', cellLoc='center', bbox=[-0.1, -0.1, 1.15, 1.15])
    table_plot.auto_set_font_size(False)
    table_plot.set_fontsize(14)
    plt.savefig('./docs/images/table.png')
    
    plt.show()

   

    
