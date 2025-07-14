import tkinter as tk
from tkinter import messagebox
import itertools

# Destination data
destination_sets = {
    "Local": [
        {"name": "Charminar", "cost": 150, "time": 2},
        {"name": "Golconda Fort", "cost": 200, "time": 3},
        {"name": "Salar Jung Museum", "cost": 120, "time": 2},
        {"name": "Ramoji Film City", "cost": 300, "time": 6},
        {"name": "Hussain Sagar Lake", "cost": 100, "time": 1.5},
        {"name": "Birla Planetarium", "cost": 120, "time": 2},
        {"name": "Nehru Zoological Park", "cost": 180, "time": 4},
        {"name": "Chowmahalla Palace", "cost": 150, "time": 2},
        {"name": "Snow World", "cost": 250, "time": 2},
    ],
    "National": [
        {"name": "India Gate", "cost": 400, "time": 4},
        {"name": "Red Fort", "cost": 350, "time": 3},
        {"name": "Gateway of India", "cost": 450, "time": 5},
        {"name": "Taj Mahal", "cost": 600, "time": 6},
    ],
    "International": [
        {"name": "Eiffel Tower, Paris", "cost": 25000, "time": 12},
        {"name": "Tokyo Disneyland", "cost": 30000, "time": 14},
        {"name": "London Eye", "cost": 28000, "time": 13},
    ],
}

# Brute-force planner (accurate selection)
def plan_trip(budget, time_limit, travel_type):
    budget = float(budget)
    time_limit = float(time_limit)
    destinations = destination_sets[travel_type]

    best_plan = []
    best_cost = 0
    best_time = 0

    for r in range(1, len(destinations) + 1):
        for combo in itertools.combinations(destinations, r):
            total_cost = sum(place['cost'] for place in combo)
            total_time = sum(place['time'] for place in combo)
            if total_cost <= budget and total_time <= time_limit:
                if total_time > best_time or (total_time == best_time and total_cost > best_cost):
                    best_plan = combo
                    best_cost = total_cost
                    best_time = total_time

    return best_plan, best_cost, best_time

# Callback function for GUI
def on_plan():
    try:
        budget = budget_entry.get()
        time_limit = time_entry.get()
        travel_type = travel_type_var.get()

        if not budget or not time_limit:
            raise ValueError("Please fill all inputs.")
        itinerary, cost, time_spent = plan_trip(budget, time_limit, travel_type)
        if itinerary:
            result = f"🧳 Travel Type: {travel_type}\n\n"
            result += "\n".join([f"- {place['name']} (₹{place['cost']}, {place['time']} hrs)" for place in itinerary])
            result += f"\n\n✅ Total Cost: ₹{cost}\n⏳ Total Time: {time_spent} hrs"
        else:
            result = "⚠️ No valid itinerary found with the given constraints."

        result_label.config(text=result)
    except ValueError as e:
        messagebox.showerror("Input Error", str(e))

# GUI setup
root = tk.Tk()
root.title("Student Travel Planner")

tk.Label(root, text="Select Travel Type:").pack()
travel_type_var = tk.StringVar(value="Local")
travel_type_menu = tk.OptionMenu(root, travel_type_var, "Local", "National", "International")
travel_type_menu.pack()

tk.Label(root, text="Enter Budget (₹):").pack()
budget_entry = tk.Entry(root)
budget_entry.pack()

tk.Label(root, text="Enter Time Available (hours):").pack()
time_entry = tk.Entry(root)
time_entry.pack()

tk.Button(root, text="Plan Trip", command=on_plan).pack(pady=10)

result_label = tk.Label(root, text="", justify="left", font=("Arial", 12))
result_label.pack(pady=10)

root.mainloop()
