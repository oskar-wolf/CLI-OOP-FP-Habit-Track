# User.py

import sqlite3

class User:
    # Represents a user with various attributes and methods for database interaction.

    def __init__(self, user_id, username, email, password, age=None, gender=None):
        # Initializes a user object with basic information.

        self.user_id = user_id
        self.username = username
        self.email = email
        self.password = password
        self.age = age
        self.gender = gender

    def save_to_database(self):
        # Saves the user's data into the database.

        conn = sqlite3.connect('goalgroove.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO User VALUES (?, ?, ?, ?, ?, ?)',
                       (self.user_id, self.username, self.email, self.password, self.age, self.gender))
        conn.commit()
        conn.close()

    @classmethod
    def get_user_by_username(cls, username):
        # Retrieves a user from the database based on their username.

        conn = sqlite3.connect('goalgroove.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM User WHERE username = ?', (username,))
        user_data = cursor.fetchone()
        conn.close()

        if user_data:
            return cls(*user_data)  # Create a user instance from the retrieved data
        else:
            return None

    @classmethod
    def login(cls, username, password):
        # Attempts to log in a user by verifying their credentials.

        user = cls.get_user_by_username(username)
        if user and user.password == password:
            return user
        else:
            return None
    
    def add_friends(self, *friend_usernames):
        # Adds friends to the user's friend list.

        conn = sqlite3.connect('goalgroove.db')
        cursor = conn.cursor()

        for friend_username in friend_usernames:
            cursor.execute('SELECT * FROM User WHERE username = ?', (friend_username,))
            friend_data = cursor.fetchone()

            if friend_data:
                cursor.execute('INSERT INTO Friendship (user_id, friend_id) VALUES (?, ?)', (self.user_id, friend_data[0]))

        conn.commit()
        conn.close()

    def post_status_update(self, status_text):
        # Posts a status update to the user's wall.

        conn = sqlite3.connect('goalgroove.db')
        cursor = conn.cursor()

        import datetime
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        cursor.execute('INSERT INTO StatusUpdate (user_id, wall_id, timestamp, text) VALUES (?, ?, ?, ?)',
                       (self.user_id, self.user_id, timestamp, status_text))

        conn.commit()
        conn.close()

    @classmethod
    def get_all_users(cls):
        # Retrieves information about all users from the database.

        conn = sqlite3.connect('goalgroove.db')
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM User')
        users_data = cursor.fetchall()

        conn.close()

        users = [cls(*user_data) for user_data in users_data]
        return users

    def get_wall_posts(self):
        # Retrieves status updates from the user's wall and their friends' walls.

        conn = sqlite3.connect('goalgroove.db')
        cursor = conn.cursor()

        cursor.execute('''
            SELECT StatusUpdate.text, StatusUpdate.timestamp, User.username
            FROM StatusUpdate
            JOIN User ON StatusUpdate.user_id = User.user_id
            WHERE StatusUpdate.user_id = ? OR StatusUpdate.user_id IN (
                SELECT friend_id FROM Friendship WHERE user_id = ?
            )
            ORDER BY StatusUpdate.timestamp DESC
        ''', (self.user_id, self.user_id))
        
        status_updates = cursor.fetchall()
        conn.close()

        return status_updates