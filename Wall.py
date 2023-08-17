# Wall.py

import sqlite3

class Wall:
    # Represents a user's wall and provides methods for retrieving wall posts in the GoalGroove application.

    def __init__(self, user_id):
        # Initializes a Wall instance with the user's ID.

        self.user_id = user_id

    def get_wall_posts(self):
        # Retrieves status updates from the user's wall and their friends' walls.

        conn = sqlite3.connect('goalgroove.db')
        cursor = conn.cursor()

        # Get status updates for the current user and their friends
        cursor.execute('''
            SELECT StatusUpdate.text, StatusUpdate.timestamp, User.username
            FROM StatusUpdate
            JOIN User ON StatusUpdate.user_id = User.user_id
            WHERE StatusUpdate.user_id = ? OR StatusUpdate.user_id IN (
                SELECT friend_id FROM Friendship WHERE user_id = ?
            )
            ORDER BY StatusUpdate.timestamp DESC
        ''', (self.user_id, self.user_id))
        
        wall_posts_data = cursor.fetchall()
        conn.close()

        # Create a list of dictionaries containing post information
        wall_posts = [{'text': row[0], 'timestamp': row[1], 'username': row[2]} for row in wall_posts_data]
        return wall_posts
