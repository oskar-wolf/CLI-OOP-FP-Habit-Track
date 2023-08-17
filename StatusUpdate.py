# StatusUpdate.py

import sqlite3
from datetime import datetime

class StatusUpdate:

    # This class represents a status update.

    def __init__(self, user_id):
        # This method initializes the status update with the user's ID.
        self.user_id = user_id

    def create_status_update(self, text):
        # This method creates a new status update and adds it to the user's wall.

        conn = sqlite3.connect('goalgroove.db')
        cursor = conn.cursor()

        # Get the user's wall ID.
        wall_id = self._get_user_wall_id(cursor)

        # Get the current timestamp.
        current_time = datetime.now()
        timestamp = current_time.strftime('%Y-%m-%d %H:%M:%S')

        # Insert the status update into the database.
        cursor.execute('INSERT INTO StatusUpdate (user_id, wall_id, text, timestamp) VALUES (?, ?, ?, ?)',
                       (self.user_id, wall_id, text, timestamp))

        conn.commit()
        conn.close()

    def _get_user_wall_id(self, cursor):
        # This method retrieves the user's wall ID from the database.

        cursor.execute('SELECT wall_id FROM Wall WHERE user_id = ?', (self.user_id,))
        wall_data = cursor.fetchone()

        if wall_data:
            # The user has a wall, return its ID.
            return wall_data[0]
        else:
            # The user doesn't have a wall, create one and return its ID.
            cursor.execute('INSERT INTO Wall (user_id) VALUES (?)', (self.user_id,))
            return cursor.lastrowid