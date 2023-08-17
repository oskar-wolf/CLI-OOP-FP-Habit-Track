import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


class Analytics:

    # This class provides methods for analyzing user data.

    def __init__(self, user_id):
        # This method initializes the analytics object with the user's ID.
        self.user_id = user_id

    def get_longest_streak(self):
        # This method gets the longest streak for each habit.

        conn = sqlite3.connect('goalgroove.db')
        cursor = conn.cursor()

        cursor.execute('''
            SELECT Habit.name, MAX(strftime('%j', date('now')) - strftime('%j', Habit.creation_date)) as streak_length
            FROM Habit
            LEFT JOIN GoalPeriod ON Habit.habit_id = GoalPeriod.habit_id
            WHERE GoalPeriod.completion_date IS NOT NULL AND Habit.user_id = ?
            GROUP BY Habit.name
        ''', (self.user_id,))
        longest_streak_data = cursor.fetchall()

        conn.close()

        # Create a dictionary of habit streaks.
        habit_streaks = {name: streak_length for name, streak_length in longest_streak_data}

        return habit_streaks