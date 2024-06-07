import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt # type: ignore
import numpy as np

# Function to plot lines and the watchman route
def plot_lines_and_route(lines, route=None):
    fig, ax = plt.subplots()
    for (m, c) in lines:
        x = np.linspace(-10, 10, 400)
        y = m * x + c
        ax.plot(x, y, label=f'y = {m:.2f}x + {c:.2f}')
    
    if route:
        route_x, route_y = zip(*route)
        ax.plot(route_x, route_y, 'ro-', label='Watchman Route')
    
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.legend()
    ax.grid(True)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('b-Link Watchman Route for 2D Lines')
    plt.show()

# Function to check if two lines are parallel
def are_parallel(line1, line2):
    return line1[0] == line2[0]

# Function to find intersection point of two lines
def intersection_point(line1, line2):
    m1, c1 = line1
    m2, c2 = line2
    if m1 == m2:  # Parallel lines don't intersect
        return None
    x = (c2 - c1) / (m1 - m2)
    y = m1 * x + c1
    return (x, y)

# Case 1: All Lines Parallel to each other
def case1_parallel_lines(lines):
    if all(are_parallel(lines[i], lines[j]) for i in range(len(lines)) for j in range(i+1, len(lines))):
        messagebox.showinfo("Result", "No watchman route exists for parallel lines.")
        plot_lines_and_route(lines)
    else:
        messagebox.showinfo("Result", "Not all lines are parallel.")

# Case 2: All lines are non-parallel
def case2_non_parallel_lines(lines):
    if not any(are_parallel(lines[i], lines[j]) for i in range(len(lines)) for j in range(i+1, len(lines))):
        messagebox.showinfo("Result", "Watchman route with at most two links exists.")
        # Select any line as starting line
        start_line = lines[0]
        # Find intersection points with all other lines
        intersections = [intersection_point(start_line, line) for line in lines if intersection_point(start_line, line)]
        # Route: start -> intersections -> turn 180 degrees -> back to start
        route = [intersections[0]] + intersections[::-1]
        plot_lines_and_route(lines, route)
    else:
        messagebox.showinfo("Result", "Not all lines are non-parallel.")

# Case 3: Mixture of Parallel and Non-Parallel Lines
def case3_mixed_lines(lines):
    # Assuming we can find a triangle with maximum area to use for the route
    max_area = 0
    best_triangle = None
    
    for i in range(len(lines)):
        for j in range(i+1, len(lines)):
            for k in range(j+1, len(lines)):
                p1 = intersection_point(lines[i], lines[j])
                p2 = intersection_point(lines[j], lines[k])
                p3 = intersection_point(lines[k], lines[i])
                if p1 and p2 and p3:
                    area = 0.5 * abs(p1[0]*(p2[1] - p3[1]) + p2[0]*(p3[1] - p1[1]) + p3[0]*(p1[1] - p2[1]))
                    if area > max_area:
                        max_area = area
                        best_triangle = [p1, p2, p3]
    
    if best_triangle:
        messagebox.showinfo("Result", "Watchman route with at most three links exists.")
        route = best_triangle + [best_triangle[0]]
        plot_lines_and_route(lines, route)
    else:
        messagebox.showinfo("Result", "No suitable triangle found.")

# Case 4: Grid Formation (Maximum Area Quadrilateral)
def case4_grid_formation(lines):
    max_area = 0
    best_quadrilateral = None
    
    for i in range(len(lines)):
        for j in range(i+1, len(lines)):
            for k in range(j+1, len(lines)):
                for l in range(k+1, len(lines)):
                    p1 = intersection_point(lines[i], lines[j])
                    p2 = intersection_point(lines[j], lines[k])
                    p3 = intersection_point(lines[k], lines[l])
                    p4 = intersection_point(lines[l], lines[i])
                    if p1 and p2 and p3 and p4:
                        # Calculate the area of the quadrilateral using the Shoelace formula
                        area = 0.5 * abs(p1[0]*p2[1] + p2[0]*p3[1] + p3[0]*p4[1] + p4[0]*p1[1]
                                         - p1[1]*p2[0] - p2[1]*p3[0] - p3[1]*p4[0] - p4[1]*p1[0])
                        if area > max_area:
                            max_area = area
                            best_quadrilateral = [p1, p2, p3, p4]
    
    if best_quadrilateral:
        messagebox.showinfo("Result", "Watchman route with at most four links exists.")
        route = best_quadrilateral + [best_quadrilateral[0]]
        plot_lines_and_route(lines, route)
    else:
        messagebox.showinfo("Result", "No suitable quadrilateral found.")

# Function to run the selected case
def run_case(case):
    lines = [(float(entries[i][0].get()), float(entries[i][1].get())) for i in range(len(entries))]
    if case == 1:
        case1_parallel_lines(lines)
    elif case == 2:
        case2_non_parallel_lines(lines)
    elif case == 3:
        case3_mixed_lines(lines)
    elif case == 4:
        case4_grid_formation(lines)
    else:
        messagebox.showerror("Error", "Invalid case selected.")

# Function to create input fields for lines
def create_input_fields():
    global entries
    num_lines = int(num_lines_entry.get())
    for widget in input_frame.winfo_children():
        widget.destroy()
    entries = []
    for i in range(num_lines):
        tk.Label(input_frame, text=f"Line {i+1} (m, c):").grid(row=i, column=0)
        m_entry = tk.Entry(input_frame)
        m_entry.grid(row=i, column=1)
        c_entry = tk.Entry(input_frame)
        c_entry.grid(row=i, column=2)
        entries.append((m_entry, c_entry))

# Function to handle custom input case
def custom_input():
    lines = [(float(entries[i][0].get()), float(entries[i][1].get())) for i in range(len(entries))]
    plot_lines_and_route(lines)

# Function to set default lines for each case
def set_default_lines(case):
    global entries
    if case == 1:
        default_lines = [(1, 1), (1, 5), (1, 3)]  # All parallel
    elif case == 2:
        default_lines = [(1, 1), (2, 3), (-1, 2)]  # All non-parallel
    elif case == 3:
        default_lines = [(1, 1), (2, 3), (-1, 2), (0.5, -1)]  # Mixed lines
    elif case == 4:
        default_lines = [(1, 0), (-1, 0), (0, -1), (2, 2),(3,4)]  # Grid formation
    else:
        default_lines = []
    
    num_lines_entry.delete(0, tk.END)
    num_lines_entry.insert(0, len(default_lines))
    create_input_fields()
    
    for i, (m, c) in enumerate(default_lines):
        entries[i][0].delete(0, tk.END)
        entries[i][0].insert(0, str(m))
        entries[i][1].delete(0, tk.END)
        entries[i][1].insert(0, str(c))

# Create the main window
root = tk.Tk()
root.title("b-Link Watchman Route")

tk.Label(root, text="Number of Lines:").grid(row=0, column=0)
num_lines_entry = tk.Entry(root)
num_lines_entry.grid(row=0, column=1)
tk.Button(root, text="Set Lines", command=create_input_fields).grid(row=0, column=2)

input_frame = tk.Frame(root)
input_frame.grid(row=1, column=0, columnspan=3)

tk.Button(root, text="Case 1: All Parallel", command=lambda: run_case(1)).grid(row=2, column=0)
tk.Button(root, text="Case 2: All Non-Parallel", command=lambda: run_case(2)).grid(row=2, column=1)
tk.Button(root, text="Case 3: Mixed Lines", command=lambda: run_case(3)).grid(row=2, column=2)
tk.Button(root, text="Case 4: Grid Formation", command=lambda: run_case(4)).grid(row=2, column=3)

#tk.Button(root, text="Custom Input", command=custom_input).grid(row=0, column=3, columnspan=3)


tk.Label(root, text="Default Inputs to Test the 4 Cases").grid(row=6, column=0, columnspan=3)

# Buttons for default lines
tk.Button(root, text="Default Case 1", command=lambda: set_default_lines(1)).grid(row=7, column=0)
tk.Button(root, text="Default Case 2", command=lambda: set_default_lines(2)).grid(row=7, column=1)
tk.Button(root, text="Default Case 3", command=lambda: set_default_lines(3)).grid(row=7, column=2)
tk.Button(root, text="Default Case 4", command=lambda: set_default_lines(4)).grid(row=7, column=3)

root.mainloop()
