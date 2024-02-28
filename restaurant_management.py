import tkinter as tk
from tkinter import ttk
import sqlite3
from datetime import datetime

class RestaurantManagementApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Restaurant Management System")

        #Connect to SQLite database
        self.conn = sqlite3.connect('restaurant.db')
        self.cursor = self.conn.cursor()

        #Create bills table
        self.cursor.execute('''
            CREATE TABLE bills( 
                id INTEGER PRIMARY KEY,
                date_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                items TEXT,
                total_amount REAL
            )             
        ''')

        # Create frames
        self.menu_frame = ttk.Frame(self.master, borderwidth=2, relief=tk.GROOVE)
        self.menu_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.bill_frame = ttk.Frame(self.master, borderwidth=2, relief=tk.GROOVE)
        self.bill_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Define cuisines and their respective menu items
        self.cuisines = {
            "American": ["Burger - $5.99", "Grilled Chicken Sandwich - $6.99", "Steak - $15.99", "Fish and Chips - $10.99", "Club Sandwich - $7.49", "BBQ Ribs - $14.99", "Veggie Burger - $6.99", "Chicken Wings - $9.99", "Buffalo Chicken Wrap - $8.49", "Fried Shrimp - $12.99"],
            "Italian": ["Pizza - $8.99", "Spaghetti - $9.99", "Caesar Salad - $7.99", "Margherita Pizza - $9.49", "Chicken Alfredo - $12.99", "Lasagna - $11.99", "Caprese Salad - $8.49", "Calzone - $10.49", "Ravioli - $10.99", "Tiramisu - $5.99"],
            "Asian": ["Sushi Roll - $12.99", "Chicken Tikka Masala - $11.99", "Shrimp Alfredo - $13.99", "Pad Thai - $10.49", "Beef Teriyaki - $14.99", "Spring Rolls - $6.99", "Miso Soup - $4.49", "Fried Rice - $8.99", "Szechuan Beef - $13.49", "Green Curry - $11.99"],
            "Mexican": ["Tacos - $7.99", "Nachos - $6.99", "Burrito - $8.49", "Enchiladas - $9.99", "Quesadilla - $6.49", "Churros - $4.99", "Guacamole - $5.49", "Fajitas - $10.99", "Mexican Rice - $3.99", "Chiles Rellenos - $11.49"]
        }

        # Add widgets to the menu frame
        self.menu_label = tk.Label(self.menu_frame, text="Menu", font=("Helvetica", 16))
        self.menu_label.pack(pady=10)

        # Create a menu section for each cuisine
        for cuisine, items in self.cuisines.items():
            cuisine_label = ttk.Label(self.menu_frame, text=cuisine, font=("Helvetica", 14))
            cuisine_label.pack(pady=5)

            cuisine_frame = ttk.Frame(self.menu_frame)
            cuisine_frame.pack()

            cuisine_listbox = tk.Listbox(cuisine_frame, width=40, height=8, selectmode=tk.MULTIPLE)
            cuisine_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            scrollbar = ttk.Scrollbar(cuisine_frame, orient=tk.VERTICAL, command=cuisine_listbox.yview)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            cuisine_listbox.config(yscrollcommand=scrollbar.set)
            

            for item in items:
                cuisine_listbox.insert(tk.END, item)

        # Add buttons for menu interaction
        self.add_to_bill_button = tk.Button(self.bill_frame, text="Add to Bill", command=self.add_to_bill)
        self.add_to_bill_button.pack(pady=5)
        
        self.clear_bill_button = tk.Button(self.bill_frame, text="Clear Bill", command=self.clear_bill)
        self.clear_bill_button.pack(pady=5)

        # Add widgets to the bill frame
        self.bill_label = tk.Label(self.bill_frame, text="Bill", font=("Helvetica", 16))
        self.bill_label.pack(pady=10)

        self.bill_text = tk.Text(self.bill_frame, width=40, height=15)
        self.bill_text.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

        # Add scrollbar to bill text widget
        self.bill_scrollbar = tk.Scrollbar(self.bill_frame, orient=tk.VERTICAL)
        self.bill_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.bill_text.config(yscrollcommand=self.bill_scrollbar.set)
        self.bill_scrollbar.config(command=self.bill_text.yview)

        self.generate_bill_button = tk.Button(self.bill_frame, text="Generate Bill", command=self.generate_bill)
        self.generate_bill_button.pack(pady=10)

    def add_to_bill(self):
        # Add selected items from menu to the bill
        selected_items = self.menu_frame.focus_get().curselection()
        for index in selected_items:
            item = self.menu_frame.focus_get().get(index)
            self.bill_text.insert(tk.END, item + "\n")

    def clear_bill(self):
        # Clear the bill text widget
        self.bill_text.delete('1.0', tk.END)

    def generate_bill(self):
        # Get all lines from the bill text widget
        bill_lines = self.bill_text.get("1.0", tk.END).split("\n")
        
        # Remove any empty lines
        bill_lines = [line.strip() for line in bill_lines if line.strip()]
        
        total = 0
        for line in bill_lines:
            # Split each line into item and price
            item, price = line.split(" - $")
            total += float(price)

        #Insert bill data into the database
        items_str = '\n'.join(bill_lines)
        self.cursor.execute(''' 
            INSERT INTO bills (date_time, items, total_amount) VALUES (?, ?, ?)

        ''', (datetime.now(), items_str, total))
        self.conn.commit()


        # Display the total in the bill section
        self.bill_text.insert(tk.END, f"\nTotal: ${total:.2f}\n")
        
def main():
    root = tk.Tk()
    app = RestaurantManagementApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

