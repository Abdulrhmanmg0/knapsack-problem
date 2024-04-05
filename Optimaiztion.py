import urllib.request


def knapsack_greedy(capacity, weights, values):

    n = len(weights)
    ratios = [(values[i] / weights[i], i) for i in range(n)]
    ratios.sort(reverse=True)
    max_value = 0
    selected_items = []
    for ratio,j in ratios:
        if capacity >= weights[j]:
            selected_items.append(j)
            capacity -= weights[j]
            max_value += values[j]
        else:
            break

    return max_value, [1 if x in selected_items else 0 for x in range(n)]     # return BestValue , SelectedItems


def knapsack_exhaustive_search(capacity, weights, values):

    n = len(weights)
    max_value = 0
    best_items = []
    for i in range(2 ** n):
        items = [j for j in range(n) if (i & (1 << j)) > 0]
        weight = sum([weights[j] for j in items])
        value = sum([values[j] for j in items])
        if weight <= capacity and value > max_value:
            max_value = value
            best_items = items
    return max_value, [1 if i in best_items else 0 for i in range(n)]


lines = []  # reading all files data from the web it might take long time
for n in range(1, 9):
    URLS = [f"https://people.sc.fsu.edu/~jburkardt/datasets/knapsack_01/p0{n}_c.txt",
            f"https://people.sc.fsu.edu/~jburkardt/datasets/knapsack_01/p0{n}_w.txt",
            f"https://people.sc.fsu.edu/~jburkardt/datasets/knapsack_01/p0{n}_p.txt",
            f"https://people.sc.fsu.edu/~jburkardt/datasets/knapsack_01/p0{n}_s.txt"]
    for i in URLS:
        url = i

        with urllib.request.urlopen(url) as response:
            file_contents = response.read().decode('utf-8')

        lines.append([int(line.strip()) for line in file_contents.splitlines()])

i, j = 0, 1
f = open("Obtimaiztion.txt",'w') # the output file
f.write("*"*127+"\n")
while i < len(lines):

    Greedy_Best, Greedy_Selected = knapsack_greedy(*lines[i], lines[i + 1], lines[i + 2]) # calling the methods
    Exact_Best, Exact_Selected = knapsack_exhaustive_search(*lines[i], lines[i + 1], lines[i + 2])

    # start formatting the output file into a table
    f.write("{:^132}".format(f"_______")+"\n")
    f.write("{:^132}".format(f"| P0{j} |")+"\n")
    f.write("{:<127}".format("_" * 127)+"\n")

    f.write("{:<15}".format(f"|  Algorithm  |")+"{:<15}".format(f"  Best Value  |")+
            "{:^73}".format(f"Selected items")+"{:<22}".format(f"|  Accuracy percentage |")+"\n")
    f.write("{:<127}".format("_" * 127)+"\n")

    f.write("{:<14}".format(f"| Brute_Force ") +"|" +"{:^14}".format(f"{Exact_Best}") + "|" +
            "{:^73}".format(f"{Exact_Selected}") + "|" + "{:^22}".format(f"%{100.00}") + "|\n")
    f.write("{:<127}".format("_" * 127)+"\n")

    f.write("{:<14}".format(f"| Greedy ") +"|" +"{:^14}".format(f"{Greedy_Best}") + "|" +
            "{:^73}".format(f"{Greedy_Selected}") + "|" + "{:^22}".format(f"%{(100 * Greedy_Best) / Exact_Best:.2f}") + "|\n")
    f.write("{:<127}".format("_" * 127)+"\n")

    f.write("{:<29}".format(f"| File ")+"|"+"{:^73}".format(f"{lines[i+3]}")+"|"+"{:^22}".format(" ")+"|\n")

    f.write("{:<127}".format("_" * 127)+"\n\n")
    f.write("*" * 127+"\n\n")

    i += 4  # number of steps
    j += 1  # number of problems

f.close()
