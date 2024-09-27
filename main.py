import math
import csv
import scipy.stats as stats
import matplotlib.pyplot as plt

def generate_period_data():
    print("Processing period data...")

    data = {}
    with open('data.csv', mode='r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            key, value = int(row[0]), int(row[1])
            data[key] = value

    values, probs, min_prob, max_prob, average, min, max, sd = process_data(data)

    generate_graph(values, probs, "Distribution of Cycle Length Probabilities", "Cycle Length (Days)", "Probabilities in %", min_prob, max_prob, average, min, max, "./docs/images/graph.png")
    generate_table(values, probs, average, sd, ["Cycle Length (Days)", "Probability in %", "Period will occur today in %"], "./docs/images/table.png")

def generate_ovulation_data():
    print("Processing ovulation data...")

    data = {}
    with open('ovulation_data.csv', mode='r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            key, value = int(row[0]), int(row[1])
            data[key] = value

    values, probs, min_prob, max_prob, average, min, max, sd = process_data(data)

    generate_graph(values, probs, "Distribution of Ovulation Probabilities", "Ovulation on Day", "Probabilities in %", min_prob, max_prob, average, min, max, "./docs/images/ovulation_graph.png")
    generate_table(values, probs, average, sd, ["Ovulation at Day", "Probability in %", "Ovulation will occur today in %"], "./docs/images/ovulation_table.png")
    
def process_data(data):
    min = float("inf")
    max = float("-inf")

    n = 0
    sum = 0
    sd_sum = 0

    probabilities = {}

    for k in data.keys():
        n += data[k]
        sum += k * data[k]

        if k < min:
            min = k

        if k > max:
            max = k

    average = sum / n

    for k in data.keys():
        sd_sum += math.pow(k - average, 2) * data[k]

    sd = math.sqrt(sd_sum / n)

    print("Average", average)
    print("Sd", sd)

    c = min

    while c <= max:
        za = c-1
        zb = c+1

        za = (za - average) / sd
        zb = (zb - average) / sd

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

    return (values, probs, min_prob, max_prob, average, min, max, sd)

def generate_graph(values, probs, title, x_label, y_label, min_prob, max_prob, average, min, max, path):
    fig, ax = plt.subplots()
    fig.set_size_inches(16, 10)

    ax.set_title(title)
    ax.plot(values, probs, marker='o', linestyle='-', color='b')
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)

    x = list(range(min, max+1))
    y = list(range(min_prob, max_prob+1))

    ax.set_xticks(x)
    ax.set_xticklabels([str(i) for i in x])

    ax.set_yticks(y)
    ax.set_yticklabels([str(round(i, 2)) for i in y])

    ax.annotate(f'Average: {average:.2f}', xy=(average, max_prob), xytext=(average - 3, max_prob - 3),
                arrowprops=dict(facecolor='black', arrowstyle='->'))

    ax.grid(True)

    plt.savefig(path)

def generate_table(values, probs, average, sd, col_labels, path):
    table_data = []
    for val, prob in zip(values, probs):
        z = (val - average) / sd
        occur_today = stats.norm.cdf(z) * 100
        table_data.append([val, f'{prob:.2f}%', f"{occur_today:.2f}%"])

    fig2, ax2 = plt.subplots(figsize=(20, 12))
    fig2.set_size_inches(20, 24)

    ax2.axis('off')  # Turn off axis for the table plot
    table_plot = ax2.table(cellText=table_data, colLabels=col_labels, loc='center', cellLoc='center', bbox=[-0.1, -0.1, 1.15, 1.15])
    table_plot.auto_set_font_size(False)
    table_plot.set_fontsize(14)
    plt.savefig(path)

if __name__ == "__main__":
    generate_period_data()
    generate_ovulation_data()

    plt.show()
