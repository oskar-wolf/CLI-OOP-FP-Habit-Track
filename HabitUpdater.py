# HabitUpdater.py

import sqlite3
from datetime import datetime

class HabitUpdater:
    # Updates goal periods for a list of habits.

    def __init__(self, user_id):
        # Initializes a HabitUpdater instance with the user's ID.

        self.user_id = user_id

    def update_goal_periods(self, habits):
        # Updates goal periods for the provided list of habits.

        conn = sqlite3.connect('goalgroove.db')
        cursor = conn.cursor()

        # Get the current date.
        current_date = datetime.now()

        for habit in habits:
            # Convert target_completion_date and creation_date to datetime objects.
            target_completion_date = datetime.strptime(habit.target_completion_date, '%Y-%m-%d')
            creation_date = datetime.strptime(habit.creation_date, '%Y-%m-%d')

            # Check if habit_id and user_id combination exists in the GoalPeriod table.
            cursor.execute('SELECT * FROM GoalPeriod WHERE user_id = ? AND habit_id = ?', (self.user_id, habit.habit_id))
            existing_data = cursor.fetchone()

            # Update or insert data in the GoalPeriod table based on habit_id and user_id.
            if existing_data:
                cursor.execute('UPDATE GoalPeriod SET completion_date = ? WHERE user_id = ? AND habit_id = ?',
                               (target_completion_date.strftime('%Y-%m-%d'), self.user_id, habit.habit_id))
            else:
                cursor.execute('INSERT INTO GoalPeriod (user_id, habit_id, completion_date) VALUES (?, ?, ?)',
                               (self.user_id, habit.habit_id, target_completion_date.strftime('%Y-%m-%d')))

            # Calculate progress percentage towards the target completion date.
            total_days = (target_completion_date - creation_date).days
            days_from_creation_date = (current_date - creation_date).days

            # Ensure progress percentage is within [0, 100].
            if total_days == 0:
                progress_percentage = 100
            else:
                progress_percentage = min((days_from_creation_date / total_days) * 100, 100)

            # Check if completion_date is past the current date.
            if target_completion_date <= current_date:
                progress_percentage = 100

            # Update progress percentage in the GoalPeriod table.
            cursor.execute('UPDATE GoalPeriod SET progress_percentage = ? WHERE user_id = ? AND habit_id = ?',
                           (progress_percentage, self.user_id, habit.habit_id))

        conn.commit()
        conn.close()
