# Brooklyn Joli
import tkinter as tk
from tkinter import messagebox
# Create a class to
class House:
    def __init__(self, house, bedrooms, lounges, bathrooms, toilets, swimming_pool, sqm):
        self.house = house
        self.bedrooms = bedrooms
        self.lounges = lounges
        self.bathrooms = bathrooms
        self.toilets = toilets
        self.swimming_pool = swimming_pool
        self.sqm = sqm

    def calculate_rental(self, risk_level):
        # Calculate features cost
        features_cost = self.house * 50 + self.bedrooms * 50 + self.lounges * 25 + self.bathrooms * 50 + \
                        self.toilets * 25 + self.swimming_pool * 150

        # Calculate sqm cost
        if self.sqm <= 150:
            sqm_cost = self.sqm * 1
        elif self.sqm <= 200:
            sqm_cost = 150 * 1 + (self.sqm - 150) * 2
        else:
            sqm_cost = 150 * 1 + 50 * 2 + (self.sqm - 200) * 2.75

        # Total features and sqm cost
        total_cost = features_cost + sqm_cost

        # Calculate management fee based on risk
        if risk_level == "low":
            management_fee_rate = 0.02
        elif risk_level == "medium":
            management_fee_rate = 0.03
        else:  # high risk
            management_fee_rate = 0.04

        # Apply management fee
        total_cost_with_fee = total_cost * (1 + management_fee_rate)

        # Apply GST
        total_cost_with_gst = total_cost_with_fee * 1.15  # 15% GST

        # Calculate weekly, monthly, and yearly rental
        weekly_rental = total_cost_with_gst
        monthly_rental = total_cost_with_gst * 4
        yearly_rental = total_cost_with_gst * 52

        return total_cost_with_gst, weekly_rental, monthly_rental, yearly_rental


class RentalAgency:  # Class to manage rental agency calculations
    def __init__(self):
        self.calculations = []

    def add_calculation(self, house, total_rental):  # Method to add a rental calculation
        self.calculations.append((house, total_rental))

    def get_statistics(self):  # Method to get statistics of rental calculations
        num_calculations = len(self.calculations)
        if num_calculations == 0:
            return 0, 0, 0
        total_rent = sum(total_rental for _, total_rental in self.calculations)
        average_rent_cost = total_rent / num_calculations
        average_sqm = sum(house.sqm for house, _ in self.calculations) / num_calculations
        return num_calculations, average_rent_cost, average_sqm

rental_agency = RentalAgency()  # Create instance of RentalAgency

def calculate_rental():  # Function to calculate rental
    # Get input values from GUI
    try:
        house = int(entries[0].get())
        bedrooms = int(entries[1].get())
        lounges = int(entries[2].get())
        bathrooms = int(entries[3].get())
        toilets = int(entries[4].get())
        swimming_pool = int(entries[5].get())
        sqm = int(entries[6].get())

        # Create House object
        house_obj = House(house, bedrooms, lounges, bathrooms, toilets, swimming_pool, sqm)

        # Get risk level
        risk_level = risk_var.get()

        # Calculate rental
        total_rental, weekly_rental, monthly_rental, yearly_rental = house_obj.calculate_rental(risk_level)

        # Add House object to agency's calculations
        rental_agency.add_calculation(house_obj, total_rental)

        # Display results
        messagebox.showinfo("Rental Calculation",
                            f"Total Rental: ${total_rental:.2f}\n"
                            f"Weekly Rental: ${weekly_rental:.2f}\n"
                            f"Monthly Rental: ${monthly_rental:.2f}\n"
                            f"Yearly Rental: ${yearly_rental:.2f}")
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numeric values.")

def show_statistics():  # Function to show rental statistics
    num_calculations, average_rent_cost, average_sqm = rental_agency.get_statistics()
    messagebox.showinfo("Key Statistics",
                        f"Number of Calculations: {num_calculations}\n"
                        f"Average Rent Cost: ${average_rent_cost:.2f}\n"
                        f"Average sqm: {average_sqm:.2f}")

def center_window(event):  # Function to center window on screen
    # Calculate screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Set window size and position
    window_width = 600
    window_height = 400
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

# Create Tkinter window
root = tk.Tk()
root.title("McLeod Rental Agency")

# Create input widgets
labels = ["House:", "Bedrooms:", "Lounges:", "Bathrooms:", "Toilets:", "Swimming Pool:", "Square Meter (sqm):"]
entries = []
for i, label_text in enumerate(labels):
    label = tk.Label(root, text=label_text)
    label.grid(row=i, column=0, padx=10, pady=5)
    entry = tk.Entry(root)
    entry.grid(row=i, column=1, padx=10, pady=5)
    entries.append(entry)

# Risk level
risk_label = tk.Label(root, text="Risk Level:")
risk_label.grid(row=len(labels), column=0, padx=10, pady=5)
risk_var = tk.StringVar(root)
risk_var.set("low")  # Default to low risk
risk_menu = tk.OptionMenu(root, risk_var, "low", "medium", "high")
risk_menu.grid(row=len(labels), column=1, padx=10, pady=5)

calculate_button = tk.Button(root, text="Calculate Rental", command=calculate_rental)
calculate_button.grid(row=len(labels)+1, column=0, columnspan=2, padx=10, pady=5)

statistics_button = tk.Button(root, text="Show Key Statistics", command=show_statistics)
statistics_button.grid(row=len(labels)+2, column=0, columnspan=2, padx=10, pady=5)

# Bind center_window function to window resize event
root.bind("<Configure>", center_window)

#end
root.mainloop()
