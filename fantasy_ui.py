import pandas as pd
import tkinter as tk
from tkinter import filedialog, ttk

def load_data():
    """Load the data file and display it in the table."""
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if not file_path:
        return  # Do nothing if no file is selected

    # Read the data into a pandas DataFrame
    df = pd.read_csv(file_path)

    # Clear existing data in the treeview
    for row in tree.get_children():
        tree.delete(row)

    # Add data to the treeview
    tree["columns"] = list(df.columns)
    tree["show"] = "headings"

    # Define column headers
    for col in df.columns:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor="center")

    # Add rows to the treeview
    for _, row in df.iterrows():
        tree.insert("", "end", values=list(row))

# Create the main application window
root = tk.Tk()
root.title("Fantasy Football Data Viewer")

# Create a frame for the UI components
frame = tk.Frame(root)
frame.pack(fill="both", expand=True, padx=10, pady=10)

# Add a button to load the file
load_button = tk.Button(frame, text="Load Fantasy Football Data", command=load_data)
load_button.pack(pady=5)

# Add a treeview to display the data
tree = ttk.Treeview(frame)
tree.pack(fill="both", expand=True)

# Run the application
root.mainloop()
