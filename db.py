import sqlite3

# Establish a connection to the database or create a new one if it doesn't exist
conn = sqlite3.connect('goalgroove.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Create the User table to store user information
cursor.execute('''
    CREATE TABLE IF NOT EXISTS User (
        user_id INTEGER PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        age INTEGER,
        gender TEXT
    )
''')

# Create the Habit table to store habit information for each user
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Habit (
        habit_id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        description TEXT,
        periodicity TEXT,
        creation_date DATE,
        target_completion_date DATE,
        FOREIGN KEY (user_id) REFERENCES User(user_id)
    )
''')

# Create the GoalPeriod table to track users' goal progress for each habit
cursor.execute('''
    CREATE TABLE IF NOT EXISTS GoalPeriod (
        goalperiod_id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        habit_id INTEGER NOT NULL,
        completion_date DATE,
        progress_percentage INTEGER,
        FOREIGN KEY (user_id) REFERENCES User(user_id),
        FOREIGN KEY (habit_id) REFERENCES Habit(habit_id)
    )
''')

# Create the Wall table to allow users to post status updates
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Wall (
        wall_id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES User(user_id)
    )
''')

# Create the StatusUpdate table to store users' status updates
cursor.execute('''
    CREATE TABLE IF NOT EXISTS StatusUpdate (
        statusupdate_id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        wall_id INTEGER NOT NULL,
        text TEXT,
        timestamp DATETIME,
        FOREIGN KEY (user_id) REFERENCES User(user_id),
        FOREIGN KEY (wall_id) REFERENCES Wall(wall_id)
    )
''')

# Create the Friendship table to track user friendships
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Friendship (
        friendship_id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        friend_id INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES User(user_id),
        FOREIGN KEY (friend_id) REFERENCES User(user_id)
    )
''')

# Sample data for the User table (for demonstration purposes)
user_data = [
    (1, 'user1', 'user1@example.com', 'password1', 25, 'Male'),
    (2, 'user2', 'user2@example.com', 'password2', 30, 'Female'),
    # Add more user data here as needed
]

# Insert data into the User table
cursor.executemany('INSERT INTO User VALUES (?, ?, ?, ?, ?, ?)', user_data)

# Sample data for the Habit table (for demonstration purposes)
habit_data = [
    (1, 1, 'Meditation', 'Practice mindfulness', 'Daily', '2023-07-28', '2023-08-15'),
    (2, 2, 'Running', 'Run 5 kilometers', '3 times a week', '2023-07-25', '2023-08-30'),
    # Add more habit data here as needed
]

# Insert data into the Habit table
cursor.executemany('INSERT INTO Habit VALUES (?, ?, ?, ?, ?, ?, ?)', habit_data)

# Sample data for the GoalPeriod table (for demonstration purposes)
goal_period_data = [
    (1, 1, 1, '2023-07-28', 80),
    (2, 2, 1, '2023-07-29', 100),
    # Add more goal period data here as needed
]

# Insert data into the GoalPeriod table
cursor.executemany('INSERT INTO GoalPeriod VALUES (?, ?, ?, ?, ?)', goal_period_data)

# Sample data for the Wall table (for demonstration purposes)
wall_data = [
    (1, 1),
    (2, 2),
    # Add more wall data here as needed
]

# Insert data into the Wall table
cursor.executemany('INSERT INTO Wall VALUES (?, ?)', wall_data)

# Sample data for the StatusUpdate table (for demonstration purposes)
status_update_data = [
    (1, 1, 1, 'Just completed my meditation session!', '2023-07-28 12:00:00'),
    (2, 2, 2, 'Went for a refreshing run today!', '2023-07-28 15:30:00'),
    # Add more status update data here as needed
]

# Insert data into the StatusUpdate table
cursor.executemany('INSERT INTO StatusUpdate VALUES (?, ?, ?, ?, ?)', status_update_data)

# Sample data for the Friendship table (for demonstration purposes)
friendship_data = [
    (1, 1, 2),
    (2, 2, 1),
    # Add more friendship data here as needed
]

# Insert data into the Friendship table
cursor.executemany('INSERT INTO Friendship VALUES (?, ?, ?)', friendship_data)

# Commit the changes and close the connection
conn.commit()
conn.close()
