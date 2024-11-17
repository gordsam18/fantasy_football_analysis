import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk, scrolledtext

# Load the data file
DATA_FILE = "2024_nfl_fantasy_football_stats.csv"

def load_data():
    """Load the data into the table when the script starts or the button is pressed."""
    try:
        # Read the data into a pandas DataFrame
        global df
        df = pd.read_csv(DATA_FILE)

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

    except FileNotFoundError:
        error_label.config(text=f"Error: File '{DATA_FILE}' not found!")
    except Exception as e:
        error_label.config(text=f"An error occurred: {str(e)}")


def question1():
    """Which position provides the most value to a fantasy football team?"""
    try:
        avg_ppr_pos = df.groupby('FantPos').apply(lambda group: group.nlargest(40, 'PPR')['PPR'].mean())
        
        # Plot the top 40 fantasy player average points by position
        avg_ppr_pos.plot(kind='bar', color='skyblue')
        plt.title('Average of the top 40 PPR Fantasy Points by Position')
        plt.xlabel('Position')
        plt.ylabel('Average of PPR Fantasy Points')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

        # Display results in the output area
        output_area.delete('1.0', tk.END)
        output_area.insert(tk.END, "Fantasy football stats by position:\n")
        output_area.insert(tk.END, avg_ppr_pos.to_string(index=True))
    except Exception as e:
        output_area.delete('1.0', tk.END)
        output_area.insert(tk.END, f"Error: {str(e)}")


def question2():
    """Which team scores the most fantasy points and how does it vary by position?"""
    try:
        # Group the fantasy teams by position
        team_position_points = df.groupby(['Tm', 'FantPos'])['PPR'].sum().reset_index(name='Total_PPR')

        # Sum teams by position
        team_points = team_position_points.groupby('Tm')['Total_PPR'].sum().reset_index()
        team_points = team_points.sort_values(by='Total_PPR', ascending=False)

        # Display results in the output area
        output_area.delete('1.0', tk.END)
        output_area.insert(tk.END, "Top Teams by Total Fantasy Points:\n")
        output_area.insert(tk.END, team_points.head(10).to_string(index=False))

        # Show breakdown by position for the top team
        top_team = team_points.iloc[0]['Tm']
        top_team_data = team_position_points[team_position_points['Tm'] == top_team]
        
        output_area.insert(tk.END, f"\n\nFantasy Points by Position for {top_team}:\n")
        output_area.insert(tk.END, top_team_data.to_string(index=False))
    except Exception as e:
        output_area.delete('1.0', tk.END)
        output_area.insert(tk.END, f"Error: {str(e)}")


def question3():
    """Which players are the most efficient in terms of fantasy points scored per touch?"""
    try:
        df['Touches'] = df['Att'] + df['Rec']  # Total touches = Rush attempts + Receptions
        df['FPPT'] = df['PPR'] / df['Touches']  # Fantasy Points Per Touch

        # Filter out players with very few touches
        filtered_df = df[df['Touches'] > 20]
        top_efficient = filtered_df[['Player', 'FantPos', 'Tm', 'Touches', 'PPR', 'FPPT']] \
                        .sort_values(by='FPPT', ascending=False).head(10)

        # Display results in the output area
        output_area.delete('1.0', tk.END)
        output_area.insert(tk.END, "Top 10 Most Efficient Players (FPPT):\n")
        output_area.insert(tk.END, top_efficient.to_string(index=False))
    except Exception as e:
        output_area.delete('1.0', tk.END)
        output_area.insert(tk.END, f"Error: {str(e)}")

def question4():
    """Which fantasy position contributes the most total touchdowns across all players?"""
    try:
        df['Total_TDs'] = df['TD.3']  # Total touchdowns

        # Group by position and calculate total touchdowns
        position_td_totals = df.groupby('FantPos')['Total_TDs'].sum().reset_index()
        position_td_totals = position_td_totals.sort_values(by='Total_TDs', ascending=False)

        # Display results in the output area
        output_area.delete('1.0', tk.END)
        output_area.insert(tk.END, "Total Touchdowns by Position:\n")
        output_area.insert(tk.END, position_td_totals.to_string(index=False))
    except Exception as e:
        output_area.delete('1.0', tk.END)
        output_area.insert(tk.END, f"Error: {str(e)}")


# Create the main application window
root = tk.Tk()
root.title("Fantasy Football Data Viewer and Analysis")

# Create a frame for the UI components
frame = tk.Frame(root)
frame.pack(fill="both", expand=True, padx=10, pady=10)

# Error label
error_label = tk.Label(frame, text="", fg="red")
error_label.pack()

# Data table
tree = ttk.Treeview(frame)
tree.pack(fill="both", expand=True)

# Add a frame for buttons
button_frame = tk.Frame(root)
button_frame.pack(fill="x", padx=10, pady=5)

# Add buttons for each question
q1_button = tk.Button(button_frame, text="Run Question 1", command=question1)
q1_button.pack(side="left", padx=5)

q2_button = tk.Button(button_frame, text="Run Question 2", command=question2)
q2_button.pack(side="left", padx=5)

q3_button = tk.Button(button_frame, text="Run Question 3", command=question3)
q3_button.pack(side="left", padx=5)

q2_button = tk.Button(button_frame, text="Run Question 4", command=question4)
q2_button.pack(side="left", padx=5)

# Output area
output_frame = tk.Frame(root)
output_frame.pack(fill="both", expand=True, padx=10, pady=5)

output_area = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD, height=10)
output_area.pack(fill="both", expand=True)

# Automatically load the data on startup
load_data()

# Run the application
root.mainloop()
