import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime


class HabitTracker:

    # This class provides methods for tracking habit progress.

    def __init__(self, user_id):
        # This method initializes the habit tracker object with the user's ID.
        self.user_id = user_id

    def plot_completion_percentage(self):
        # This method plots a bar chart showing the completion percentage for each habit.

        habit_summary = self.get_habit_summary()

        if habit_summary:
            # Get habit names for plotting.
            conn = sqlite3.connect('goalgroove.db')
            cursor = conn.cursor()
            cursor.execute('SELECT habit_id, name FROM Habit WHERE user_id = ?', (self.user_id,))
            habit_names_data = cursor.fetchall()
            conn.close()
            habit_names = {hid: name for hid, name in habit_names_data}

            # Extract data for plotting.
            habits = [habit_names[habit_id] for habit_id in habit_summary.keys()]
            completion_percentages = [data['completion_percentage'] for data in habit_summary.values()]

            # Create a bar chart with a custom color scheme.
            plt.figure(figsize=(10, 6))
            plt.bar(habits, completion_percentages, color='skyblue')

            plt.xlabel('Habits')
            plt.ylabel('Completion Percentage (%)')
            plt.title('Completion Percentage for Habits')
            plt.xticks(rotation=45, ha='right')

            # Add grid lines.
            plt.grid(axis='y', linestyle='--', alpha=0.7)

            # Set y-axis limit to 100.
            plt.ylim(0, 100)

            # Show the plot with a neat layout.
            plt.tight_layout()
            plt.show()
        else:
            print("No habits found or no summary available.")

    def get_habit_summary(self):
        # This method gets the average progress percentage for each habit.

        conn = sqlite3.connect('goalgroove.db')
        cursor = conn.cursor()

        cursor.execute('''
            SELECT habit_id, AVG(progress_percentage) as completion_percentage
            FROM GoalPeriod
            WHERE user_id = ?
            GROUP BY habit_id
        ''', (self.user_id,))
        habit_summary_data = cursor.fetchall()

        conn.close()

        habit_summary = {row[0]: {'completion_percentage': row[1]} for row in habit_summary_data}
        return habit_summary