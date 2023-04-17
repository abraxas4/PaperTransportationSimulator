# Import necessary libraries
import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Function to plot paper movement based on given parameters
def plot_paper_movement(time_duration, initial_speed, paper_length, Y_points, speed_changes):
    # Print start markers
    print("// ******************** //")
    print("// ****** Start ******* //")
    print("// ******************** //")
    # Add 0 to the beginning of Y_points list
    Y_points = [0] + Y_points
    print("Y_points given = ", Y_points);
    # Create X_axis_points using numpy's arange function
    X_axis_points = np.arange(0, time_duration + 100, 100)
    #print("X_axis_points = ", X_axis_points);
    # Create speeds list
    speeds = [0] + [initial_speed] + speed_changes
    print("speeds given = ", speeds);
    # Initialize X_points list
    X_points = [0]
    prevX = 0
    prevY = 0
    # Calculate X_points based on Y_points and speeds
    for i in range(1, len(Y_points)):
        print("\t prev = (", prevX, ",", prevY, ")")
        Y = Y_points[i]
        speed = speeds[i]
        X = prevX + int((Y-prevY) / speed * 1000)
        print("\t Y = ", Y, ", speed = ", speed, "-> X = ", X)
        print("\t next = (", X, ",", Y, ")")
        X_points.append(X)
        prevX = X
        prevY = Y
        print("\n")

    # Add time_duration to X_points list
    X_points.append(time_duration)
    print("3-0. X_points = ", X_points);
    print("3-1. Y_points = ", Y_points);
    # Calculate the last Y_point
    lastY = Y_points[-1] + (X_points[-1]-X_points[-2])*speeds[-1]/1000
    print("4. lastY = ", lastY, " = ", Y_points[-1], "+", X_points[-1], "*" , speeds[-1], "/1000")
    # Add the last Y_point to Y_points list
    Y_points.append(lastY)
    print("5-0. X_points = ", X_points);
    print("5-1. Y_points = ", Y_points);

    # Create numpy arrays for LE and TE points
    le_points = np.array([X_points, Y_points]).T
    print("6. le_points = \n", le_points);
    te_points = le_points - (0, paper_length)
    print("7. te_points = \n", te_points);

    # Create a plot with LE and TE points
    fig, ax = plt.subplots()
    ax.plot(le_points[:, 0], le_points[:, 1], label="LE")
    ax.plot(te_points[:, 0], te_points[:, 1], label="TE")

    # Set plot labels and grid
    ax.set_xlabel("Time [ms]")
    ax.set_ylabel("Position [mm]")
    ax.legend()
    ax.grid(True)
    
    
    # Add annotations for change points
    for i, X_cur in enumerate(X_points):
        print("Loop #", i, "X_cur = X = ", X_cur)
        le_y = Y_points[i]
        te_y = le_y - paper_length
        # Add annotations for change points and differences
        ax.annotate(f"({X_cur}, {le_y})", xy=(X_cur, le_y), xytext=(X_cur + 20, le_y + 20),
                    arrowprops=dict(facecolor='black', arrowstyle='->'))
        ax.annotate(f"({X_cur}, {te_y})", xy=(X_cur, te_y), xytext=(X_cur + 20, te_y - 20),
                    arrowprops=dict(facecolor='black', arrowstyle='->'))

        # Add annotations for differences between change points and draw lines
        if i > 0:
            X_prev, prev_le_y = X_points[i - 1], Y_points[i - 1]
            diff_x = X_cur - X_prev
            diff_y = le_y - prev_le_y
            mid_x = (X_cur + X_prev) / 2
            mid_y = (le_y + prev_le_y) / 2
            ax.annotate(f"Δx: {diff_x} ms\nΔy: {diff_y} mm", xy=(mid_x, mid_y - 40),
                        xytext=(mid_x, prev_le_y - 40),
                        bbox=dict(boxstyle="round,pad=0.3", edgecolor="black", facecolor="white", alpha=0.5))

            # Draw dashed lines for the differences
            ax.hlines(y=prev_le_y, xmin=X_prev, xmax=X_cur, colors='red', linestyles='dashed')
            print("\t dashed Line Horizonal: ", "(", X_prev, ",", prev_le_y, ") -> ", "(", X_cur, ",", prev_le_y, ")")

            ax.vlines(x=X_cur, ymin=prev_le_y, ymax=le_y, colors='red', linestyles='dashed')
            print("\t dashed Line Verical: ", "(", X_cur, ",", prev_le_y, ") -> ", "(", X_cur, ",", le_y, ")")

    return fig

# Function to draw the plot using the input values
def draw_plot():
    time_duration = int(time_duration_entry.get())
    initial_speed = int(initial_speed_entry.get())
    paper_length = int(paper_length_entry.get())
    Y_points = [int(le_change_position1_entry.get()), int(le_change_position2_entry.get())]
    speed_changes = [int(speed_change1_entry.get()), int(speed_change2_entry.get())]

    fig = plot_paper_movement(time_duration, initial_speed, paper_length, Y_points, speed_changes)

    canvas.figure = fig
    canvas.draw()

# Initialize the tkinter application
root = tk.Tk()
root.title("Paper Movement Plotter")

# Create a frame for the labels and entries
input_frame = tk.Frame(root)
input_frame.pack(side=tk.TOP, padx=10, pady=10)

# Create labels and entries for the input values
# Labels
time_duration_label = tk.Label(input_frame, text="Time Duration [ms]:")
initial_speed_label = tk.Label(input_frame, text="Initial Speed [mm/s]:")
paper_length_label = tk.Label(input_frame, text="Paper Length [mm]:")
le_change_position1_label = tk.Label(input_frame, text="LE Position to Change Speed 1 [mm]:")
speed_change1_label = tk.Label(input_frame, text="Speed After Change 1 [mm/s]:")
le_change_position2_label = tk.Label(input_frame, text="LE Position to Change Speed 2 [mm]:")
speed_change2_label = tk.Label(input_frame, text="Speed After Change 2 [mm/s]:")

time_duration_label.grid(row=0, column=0)
initial_speed_label.grid(row=1, column=0)
paper_length_label.grid(row=2, column=0)
le_change_position1_label.grid(row=3, column=0)
speed_change1_label.grid(row=4, column=0)
le_change_position2_label.grid(row=5, column=0)
speed_change2_label.grid(row=6, column=0)

# Entries
time_duration_entry = tk.Entry(input_frame)
initial_speed_entry = tk.Entry(input_frame)
paper_length_entry = tk.Entry(input_frame)
le_change_position1_entry = tk.Entry(input_frame)
speed_change1_entry = tk.Entry(input_frame)
le_change_position2_entry = tk.Entry(input_frame)
speed_change2_entry = tk.Entry(input_frame)

time_duration_entry.insert(0, "410")
initial_speed_entry.insert(0, "500")
paper_length_entry.insert(0, "100")
le_change_position1_entry.insert(0, "10")
speed_change1_entry.insert(0, "1000")
le_change_position2_entry.insert(0, "200")
speed_change2_entry.insert(0, "500")

time_duration_entry.grid(row=0, column=1)
initial_speed_entry.grid(row=1, column=1)
paper_length_entry.grid(row=2, column=1)
le_change_position1_entry.grid(row=3, column=1)
speed_change1_entry.grid(row=4, column=1)
le_change_position2_entry.grid(row=5, column=1)
speed_change2_entry.grid(row=6, column=1)

# Create the plot button and bind it to the draw_plot function
plot_button = tk.Button(input_frame, text="Draw Plot", command=draw_plot)
plot_button.grid(row=7, column=0, columnspan=2)

# Create an empty Figure and Canvas for the plot initially
fig, _ = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)

# Start the tkinter main loop
root.mainloop()