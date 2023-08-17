import sqlite3

class Habit:
    def __init__(self, user_id, name, description, periodicity, target_completion_date, creation_date, habit_id=None):
        # Initialize a Habit object with provided attributes.
        # Set object attributes.
        self.habit_id = habit_id
        self.user_id = user_id
        self.name = name
        self.description = description
        self.periodicity = periodicity
        self.target_completion_date = target_completion_date
        self.creation_date = creation_date

    def save_to_database(self):
        # Establish a connection to the SQLite database
        conn = sqlite3.connect('goalgroove.db')
        cursor = conn.cursor()

        # Insert a new record into the "Habit" table with provided values
        cursor.execute('INSERT INTO Habit (user_id, name, description, periodicity, creation_date, target_completion_date) VALUES (?, ?, ?, ?, ?, ?)',
                    (self.user_id, self.name, self.description, self.periodicity, self.creation_date, self.target_completion_date))

        # Retrieve the last inserted row ID (habit_id) and set it to the object attribute
        self.habit_id = cursor.lastrowid

        # Commit the changes to the database
        conn.commit()

        # Close the connection to the database
        conn.close()



    @classmethod
    def get_habit_by_id(cls, habit_id):
        # Establish a connection to the SQLite database
        conn = sqlite3.connect('goalgroove.db')
        cursor = conn.cursor()

        # Execute a SELECT query to retrieve habit data by habit_id
        cursor.execute('SELECT * FROM Habit WHERE habit_id = ?', (habit_id,))
        habit_data = cursor.fetchone()

        # Close the connection to the database
        conn.close()

        # If habit_data is not None (habit exists), create and return a Habit object
        if habit_data:
            habit = cls(habit_data[1], habit_data[2], habit_data[3], habit_data[4], habit_data[5], habit_data[6], habit_data[0])
            return habit
        else:
            # If habit_data is None (habit does not exist), return None
            return None


    @classmethod
    def get_habits_by_user_id(cls, user_id):
        # Establish a connection to the SQLite database
        conn = sqlite3.connect('goalgroove.db')
        cursor = conn.cursor()

        # Execute a SELECT query to retrieve habits data by user_id
        cursor.execute('SELECT habit_id, user_id, name, description, periodicity, target_completion_date, creation_date FROM Habit WHERE user_id = ?', (user_id,))
        habits_data = cursor.fetchall()

        # Close the connection to the database
        conn.close()

        habits = []
        for habit_data in habits_data:
            # Create a Habit object for each retrieved habit_data
            # Explicitly specify the order of attributes when constructing the Habit object
            habit = cls(habit_data[1], habit_data[2], habit_data[3], habit_data[4], habit_data[5], habit_data[6], habit_data[0])
            habits.append(habit)

        return habits


    
    def update_habit(self):
        # Print a debug message indicating the habit ID being updated
        print(f"Updating Habit with ID: {self.habit_id}")
        
        # Establish a connection to the SQLite database
        conn = sqlite3.connect('goalgroove.db')
        cursor = conn.cursor()

        # Execute an UPDATE query to modify habit data based on habit_id
        cursor.execute('UPDATE Habit SET name = ?, description = ?, periodicity = ?, target_completion_date = ? WHERE habit_id = ?',
                    (self.name, self.description, self.periodicity, self.target_completion_date, self.habit_id))

        # Commit the changes to the database
        conn.commit()

        # Close the connection to the database
        conn.close()


    def delete_habit(self):
        # Establish a connection to the SQLite database
        conn = sqlite3.connect('goalgroove.db')
        cursor = conn.cursor()

        # Delete the habit from the Habit table based on habit_id
        cursor.execute('DELETE FROM Habit WHERE habit_id = ?', (self.habit_id,))

        # Delete the corresponding goal periods from the GoalPeriod table based on habit_id
        cursor.execute('DELETE FROM GoalPeriod WHERE habit_id = ?', (self.habit_id,))

        # Commit the changes to the database
        conn.commit()

        # Close the connection to the database
        conn.close()


    @staticmethod
    def get_habit_name_by_id(habit_id):
        # Establish a connection to the SQLite database
        conn = sqlite3.connect('goalgroove.db')
        cursor = conn.cursor()

        # Execute a SELECT query to retrieve the name of a habit by habit_id
        cursor.execute('SELECT name FROM Habit WHERE habit_id = ?', (habit_id,))
        habit_data = cursor.fetchone()

        # Close the connection to the database
        conn.close()

        # If habit_data is not None (habit exists), return the habit name
        if habit_data:
            return habit_data[0]
        else:
            # If habit_data is None (habit does not exist), return None
            return None

    