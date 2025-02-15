import matplotlib.animation as animation
import matplotlib.pyplot as plt

# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

x_index = 0
xs = []
ys = []


def add_brain_measure(brain_activity):
    global x_index, xs, ys
    x_index += 1
    xs.append(x_index)
    ys.append(brain_activity)


# Initialize communication with TMP102
i = 0


# This function is called periodically from FuncAnimation
def plot_data(a, _, _2):
    global xs, ys, i

    i += 1

    # # Add x and y to lists
    # xs.append(i)
    # ys.append(random.randrange(0, 100))

    # Limit x and y lists to 20 items
    xs = xs[-100:]
    ys = ys[-100:]

    # Draw x and y lists
    ax.clear()
    ax.plot(xs, ys)

    # Format plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('Brainwavez')
    plt.ylabel('Activity')


ani = 0
def start_animation():
    global ani
    # Set up plot to call animate() function periodically
    ani = animation.FuncAnimation(fig, plot_data, fargs=(50, 50), interval=50)
    plt.show()