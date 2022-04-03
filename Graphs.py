import subprocess
import pandas as pd
import matplotlib.pyplot as plt


trace_files = ["traces/gcc_trace.txt",
               "traces/jpeg_trace.txt",
               "traces/perl_trace.txt"]
benchmarks = ["gcc", "jpeg", "perl"]

# Part 1 - b vs Miss Prediction Rate - Smith
miss_prediction_rates = [[] for i in trace_files]
for b in range(1, 7):
    for i, trace_file in enumerate(trace_files):
        command = "python3 main.py smith {} {}".format(b, trace_file)
        output = subprocess.check_output(command, shell=True)
        output = output.decode("utf-8")
        index = output.split().index("rate:")
        val = float(output.split()[index + 1].split("%")[0])
        miss_prediction_rates[i].append(val)


print("\n\nSmith Table:")
miss_prediction_rates = pd.DataFrame(miss_prediction_rates)
print(miss_prediction_rates)


for x in range(3):
    t = benchmarks[x] + ", smith"
    plt.title(t)
    plt.xlabel("b")
    plt.ylabel("Misprediction Rate")
    plt.xticks(list(range(1, 7)))
    plt.yticks(miss_prediction_rates.iloc[x])
    plt.plot(list(range(1, 7)), miss_prediction_rates.iloc[x], marker='o')
    plt.savefig(t + ".png")
    plt.clf()

# Part 2 - m vs Miss Prediction Rate - Bimodal
miss_prediction_rates = [[] for i in trace_files]
for m in range(7, 13):
    for i, trace_file in enumerate(trace_files):
        command = "python3 main.py bimodal {} {}".format(m, trace_file)
        output = subprocess.check_output(command, shell=True)
        output = output.decode("utf-8")
        index = output.split().index("rate:")
        val = float(output.split()[index + 1].split("%")[0])
        miss_prediction_rates[i].append(val)


print("\n\nBimodal Table:")
miss_prediction_rates = pd.DataFrame(miss_prediction_rates)
print(miss_prediction_rates)


for x in range(3):
    t = benchmarks[x] + ", bimodal"
    plt.title(t)
    plt.xlabel("m")
    plt.ylabel("Misprediction Rate")
    plt.xticks(list(range(7, 13)))
    plt.yticks(miss_prediction_rates.iloc[x])
    plt.plot(list(range(7, 13)), miss_prediction_rates.iloc[x], marker='o')
    plt.savefig(t + ".png")
    plt.clf()

# Part 3 - m vs Miss Prediction Rate - Gshare
miss_prediction_rates = [[] for i in trace_files]
print("\n\nGshare Tables")
for i, trace_file in enumerate(trace_files):
    t = benchmarks[i] + ", gshare"
    plt.title(t)
    plt.xlabel("m")
    plt.ylabel("Misprediction Rate")
    miss_prediction_rates = [[] for i in range(7, 13)]
    m_values = list(range(7, 13))
    for i_m, m in enumerate(m_values):
        # n lists
        miss_prediction_rates_for_n = []
        for i, n in enumerate(list(range(2, m + 1, 2))):
            command = "python3 main.py gshare {} {} {}".format(m, n, trace_file)
            output = subprocess.check_output(command, shell=True)
            output = output.decode("utf-8")
            index = output.split().index("rate:")
            val = float(output.split()[index + 1].split("%")[0])
            miss_prediction_rates_for_n.append(val)
        miss_prediction_rates[i_m].extend(miss_prediction_rates_for_n)
    miss_prediction_rates = pd.DataFrame(miss_prediction_rates)
    print("\n", t)
    print(miss_prediction_rates)
    for i_m, m in enumerate(m_values):
        plt.plot(m_values, miss_prediction_rates[i_m], marker='o')
    plt.legend(["n=" + str(i) for i in range(2, 13, 2)])
    plt.savefig(t + ".png")
    plt.clf()
