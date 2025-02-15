import numpy as np

data = []
i = 0


while True:
    i += 1
    data.append(i)

    latest_data = np.array(data[-100:])
    diffs = np.diff(latest_data)
    avg_diff = np.mean(diffs)

    print("Average difference:", avg_diff)
    if avg_diff < 0:
        print("Overall trend: Declining")
    elif avg_diff == 0:
        print("Overall trend: Flat")
    else:
        print("Overall trend: Increasing")