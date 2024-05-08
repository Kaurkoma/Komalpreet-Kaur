import tkinter as tk
from tkinter import messagebox
import csv
import json
import datetime

class TripManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Trip Management System")

        self.create_trip_fields()
        self.create_traveller_fields()
        self.create_buttons()
        self.create_listboxes()

    def create_trip_fields(self):
        tk.Label(self.root, text="Trip Name:", font=("Arial", 12)).grid(row=0, column=0, sticky="e")
        self.trip_name_entry = tk.Entry(self.root, font=("Arial", 12))
        self.trip_name_entry.grid(row=0, column=1)

        tk.Label(self.root, text="Start Date (YYYY-MM-DD):", font=("Arial", 12)).grid(row=1, column=0, sticky="e")
        self.start_date_entry = tk.Entry(self.root, font=("Arial", 12))
        self.start_date_entry.grid(row=1, column=1)

        tk.Label(self.root, text="Duration (days):", font=("Arial", 12)).grid(row=2, column=0, sticky="e")
        self.duration_entry = tk.Entry(self.root, font=("Arial", 12))
        self.duration_entry.grid(row=2, column=1)

        tk.Label(self.root, text="Contact Info:", font=("Arial", 12)).grid(row=3, column=0, sticky="e")
        self.contact_info_entry = tk.Entry(self.root, font=("Arial", 12))
        self.contact_info_entry.grid(row=3, column=1)

        tk.Label(self.root, text="Coordinator:", font=("Arial", 12)).grid(row=4, column=0, sticky="e")
        self.coordinator_entry = tk.Entry(self.root, font=("Arial", 12))
        self.coordinator_entry.grid(row=4, column=1)

    def create_traveller_fields(self):
        tk.Label(self.root, text="Traveller Name:", font=("Arial", 12)).grid(row=5, column=0, sticky="e")
        self.traveller_name_entry = tk.Entry(self.root, font=("Arial", 12))
        self.traveller_name_entry.grid(row=5, column=1)

        tk.Label(self.root, text="Address:", font=("Arial", 12)).grid(row=6, column=0, sticky="e")
        self.address_entry = tk.Entry(self.root, font=("Arial", 12))
        self.address_entry.grid(row=6, column=1)

        tk.Label(self.root, text="DOB (YYYY-MM-DD):", font=("Arial", 12)).grid(row=7, column=0, sticky="e")
        self.dob_entry = tk.Entry(self.root, font=("Arial", 12))
        self.dob_entry.grid(row=7, column=1)

        tk.Label(self.root, text="Emergency Contact:", font=("Arial", 12)).grid(row=8, column=0, sticky="e")
        self.emergency_contact_entry = tk.Entry(self.root, font=("Arial", 12))
        self.emergency_contact_entry.grid(row=8, column=1)

        tk.Label(self.root, text="ID No:", font=("Arial", 12)).grid(row=9, column=0, sticky="e")
        self.gov_id_entry = tk.Entry(self.root, font=("Arial", 12))
        self.gov_id_entry.grid(row=9, column=1)

    def create_buttons(self):
        self.create_trip_button = tk.Button(self.root, text="Create Trip", command=self.create_trip, font=("Arial", 12))
        self.create_trip_button.grid(row=10, column=0, pady=10)

        self.create_traveller_button = tk.Button(self.root, text="Create Traveller", command=self.create_traveller,
                                                 font=("Arial", 12))
        self.create_traveller_button.grid(row=10, column=1, pady=10)

        self.delete_button = tk.Button(self.root, text="Delete", command=self.delete_selected_item, font=("Arial", 12))
        self.delete_button.grid(row=10, column=2, pady=10)

        self.edit_button = tk.Button(self.root, text="Edit", command=self.edit_selected_item, font=("Arial", 12))
        self.edit_button.grid(row=10, column=3, pady=10)

        self.close_button = tk.Button(self.root, text="Close", command=self.root.quit, font=("Arial", 12))
        self.close_button.grid(row=10, column=4, pady=10)

    def create_listboxes(self):
        self.trip_listbox = tk.Listbox(self.root, width=100, font=("Arial", 12))
        self.trip_listbox.grid(row=11, column=0, columnspan=5, padx=10, pady=10)

        self.traveller_listbox = tk.Listbox(self.root, width=100, font=("Arial", 12))
        self.traveller_listbox.grid(row=12, column=0, columnspan=5, padx=10, pady=10)

    def create_trip(self):
        trip_name = self.trip_name_entry.get()
        start_date = self.start_date_entry.get()
        duration = self.duration_entry.get()
        contact_info = self.contact_info_entry.get()
        coordinator = self.coordinator_entry.get()

        if not self.validate_trip_fields(duration, contact_info, start_date):
            return

        trip_details = f"Trip Name: {trip_name}, Start Date: {start_date}, Duration: {duration}, " \
                       f"Contact Info: {contact_info}, Coordinator: {coordinator}"
        self.trip_listbox.insert(tk.END, trip_details)

        with open('trips.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([trip_name, start_date, duration, contact_info, coordinator])

    def create_traveller(self):
        traveller_name = self.traveller_name_entry.get()
        address = self.address_entry.get()
        dob = self.dob_entry.get()
        emergency_contact = self.emergency_contact_entry.get()
        gov_id = self.gov_id_entry.get()

        if not self.validate_traveller_fields(dob, emergency_contact, gov_id):
            return

        traveller_details = f"Name: {traveller_name}, Address: {address}, DOB: {dob}, " \
                            f"Emergency Contact: {emergency_contact}, Gov ID: {gov_id}"
        self.traveller_listbox.insert(tk.END, traveller_details)

        traveller_data = {
            'Name': traveller_name,
            'Address': address,
            'DOB': dob,
            'Emergency Contact': emergency_contact,
            'Gov ID': gov_id
        }
        with open('travellers.json', 'a') as jsonfile:
            json.dump(traveller_data, jsonfile, indent=4)

    def validate_trip_fields(self, duration, contact_info, start_date):
        try:
            int(duration)
        except ValueError:
            messagebox.showerror("Error", "Duration must be a number.")
            return False

        if len(contact_info)!= 10 or not contact_info.isdigit():
            messagebox.showerror("Error", "Contact Info must be a 10-digit number.")
            return False

        try:
            datetime.datetime.strptime(start_date, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Error", "Date of Start must be a valid datetime.")
            return False

        return True

    def validate_traveller_fields(self, dob, emergency_contact, gov_id):
        try:
            datetime.datetime.strptime(dob, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Error", "DOB must be a valid datetime.")
            return False

        if len(emergency_contact)!= 10 or not emergency_contact.isdigit():
            messagebox.showerror("Error", "Emergency Contact must be a 10-digit number.")
            return False

        if not (len(gov_id) == 10 or len(gov_id) == 12) or not gov_id.isdigit():
            messagebox.showerror("Error", "ID No must be a 10 or 12-digit string.")
            return False

        return True

    def delete_selected_item(self):
        selected_index = self.trip_listbox.curselection()
        if selected_index:
            self.trip_listbox.delete(selected_index)
        else:
            messagebox.showinfo("Information", "Please select an item to delete.")

    def edit_selected_item(self):
        # Clear all entries in trip and traveller fields
        self.clear_entries()
        messagebox.showinfo("Information", "All entries have been cleared.")

    def clear_entries(self):
        self.trip_name_entry.delete(0, tk.END)
        self.start_date_entry.delete(0, tk.END)
        self.duration_entry.delete(0, tk.END)
        self.contact_info_entry.delete(0, tk.END)
        self.coordinator_entry.delete(0, tk.END)
        self.traveller_name_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)
        self.dob_entry.delete(0, tk.END)
        self.emergency_contact_entry.delete(0, tk.END)
        self.gov_id_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = TripManagementApp(root)
    root.mainloop()
