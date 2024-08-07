import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
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

# Function to find the maximum area triangle
def find_max_area_triangle(lines):
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
    
    return best_triangle

# Case 1: All Lines Parallel to each other
def case1_parallel_lines(lines, b):
    messagebox.showinfo("Result", "No watchman route exists for parallel lines.")
    plot_lines_and_route(lines)

# Case 2: Mixture of Parallel and Non-Parallel Lines
def case2_mixed_lines(lines, b):
    # Check if there exists a line that intersects every other line
    potential_line = None
    for i in range(len(lines)):
        intersects_all = True
        for j in range(len(lines)):
            if i != j:  # Exclude comparing a line with itself
                if not intersection_point(lines[i], lines[j]):
                    intersects_all = False
                    break
        if intersects_all:
            potential_line = lines[i]
            break
    
    if potential_line:
        messagebox.showinfo("Result", "Watchman route with two links exists.")
        start_line = potential_line
        intersections = [intersection_point(start_line, line) for line in lines if intersection_point(start_line, line)]
        route = [intersections[0]] + intersections[::-1]
        plot_lines_and_route(lines, route)
    else:
        best_triangle = find_max_area_triangle(lines)
        
        if best_triangle:
            if b is not None and b < 3:
                messagebox.showinfo("Result", f"A watchman route with {b} link(s) is not possible for mixed lines.")
                return
            messagebox.showinfo("Result", "Watchman route with at most three links exists.")
            route = best_triangle + [best_triangle[0]]
            plot_lines_and_route(lines, route)
        else:
            messagebox.showinfo("Result", "No suitable triangle found.")

# Case 3: Grid Formation
def case3_grid_formation(lines, b):
    # Sort lines by slope (first value in each tuple)
    slope_1_lines = []
    slope_2_lines = []
    m = lines[0][0]
    for line in lines:
        if m == line[0]:
            slope_1_lines.append(line)
        else:
            slope_2_lines.append(line)
    
    # Sort lines by intercept (c) in descending order
    slope_1_lines.sort(key=lambda x: x[1], reverse=True)
    slope_2_lines.sort(key=lambda x: x[1], reverse=True)
    
    outer1 = slope_1_lines[0]
    outer2 = slope_1_lines[-1]
    outer3 = slope_2_lines[0]
    outer4 = slope_2_lines[-1]

    # Calculate intersection points
    p1 = intersection_point(outer1, outer3)
    p2 = intersection_point(outer1, outer4)
    p3 = intersection_point(outer2, outer4)
    p4 = intersection_point(outer2, outer3)

    if p1 and p2 and p3 and p4:
        # Calculate the area of the quadrilateral using the Shoelace formula
        area = 0.5 * abs(p1[0]*p2[1] + p2[0]*p3[1] + p3[0]*p4[1] + p4[0]*p1[1]
                         - p1[1]*p2[0] - p2[1]*p3[0] - p3[1]*p4[0] - p4[1]*p1[0])
        if area > 0:
            if b is not None and b < 4:
                messagebox.showinfo("Result", f"A watchman route with {b} link(s) is not possible for grid formation.")
                return
            messagebox.showinfo("Result", "Watchman route with at most four links exists.")
            route = [p1, p2, p3, p4, p1]
            plot_lines_and_route(lines, route)
        else:
            messagebox.showinfo("Result", "Quadrilateral found with very less area.")
            route = [p1, p2, p3, p4, p1]
            plot_lines_and_route(lines, route)
    else:
        messagebox.showinfo("Result", "No suitable quadrilateral found.")

# Function to automatically detect the case
def detect_case(lines, b):
    all_parallel = all(are_parallel(lines[i], lines[j]) for i in range(len(lines)) for j in range(i+1, len(lines)))
    all_non_parallel = not any(are_parallel(lines[i], lines[j]) for i in range(len(lines)) for j in range(i+1, len(lines)))

    if all_parallel:
        case1_parallel_lines(lines, b)
    else:
        case2_mixed_lines(lines, b)
        if len(set(line[0] for line in lines)) == 2:  # Check for grid formation
            case3_grid_formation(lines, b)

# Function to create input fields for lines
def create_input_fields():
    global entries
    num_lines = int(num_lines_entry.get())
    for widget in input_frame.winfo_children():
        widget.destroy()
    entries = []
    
    for i in range(num_lines):
        tk.Label(input_frame, text=f"Line {i+1} (Slope, Intercept):").grid(row=i, column=0)
        m_entry = tk.Entry(input_frame)
        m_entry.grid(row=i, column=1)
        c_entry = tk.Entry(input_frame)
        c_entry.grid(row=i, column=2)
        entries.append((m_entry, c_entry))

# Function to handle custom input case
def custom_input():
    lines = [(float(entries[i][0].get()), float(entries[i][1].get())) for i in range(len(entries))]
    b = b_entry.get()
    b = int(b) if b else None
    detect_case(lines, b)

# Function to set default lines for testing
def set_default_lines(case):
    global entries
    if case == 1:
        default_lines = [(1, 1), (1, 5), (1, 3)]  # All parallel
    elif case == 2:
        default_lines = [(1, 1), (2, 3), (-1, 2), (0.5, -1), (1, 4)]  # Mixed lines
    elif case == 4:
        default_lines = [(1,4),(1,8),(-0.5,1),(-0.5,5),(8,8),(8,12)] #sample trinagle
    elif case == 3:
        default_lines = [(1, 4), (1, 3), (1, 6), (1, 7), (5, 1), (5, 7)]  # Grid formation
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
root.title("Minimum Link Watchman Route")

tk.Label(root, text="Number of Lines:").grid(row=0, column=0)
num_lines_entry = tk.Entry(root)
num_lines_entry.grid(row=0, column=1)
tk.Button(root, text="Set Lines", command=create_input_fields).grid(row=0, column=2)

tk.Label(root, text="Optional: Maximum number of links (b):").grid(row=1, column=0)
b_entry = tk.Entry(root)
b_entry.grid(row=1, column=1)

tk.Label(root, text ="The equation of line is mx + c, in which m is the slope and c is the intercept").grid(row = 2, column = 0, columnspan = 3)
input_frame = tk.Frame(root)
input_frame.grid(row=3, column=0, columnspan=3)

tk.Button(root, text="Check Watchman Route", command=custom_input).grid(row=4, column=0, columnspan=3)

tk.Label(root, text="Don't want to set lines? No worries, click on Sample case buttons to test the different Cases").grid(row=7, column=0, columnspan=3)

# Buttons for default lines
tk.Button(root, text="Sample Case 1", command=lambda: set_default_lines(1)).grid(row=8, column=0)
tk.Button(root, text="Sample Case 2", command=lambda: set_default_lines(2)).grid(row=8, column=1)
tk.Button(root, text="Sample Case 3", command=lambda: set_default_lines(3)).grid(row=8, column=2)
tk.Button(root, text="Sample Case 4", command=lambda: set_default_lines(4)).grid(row=8, column=3)

root.mainloop()
