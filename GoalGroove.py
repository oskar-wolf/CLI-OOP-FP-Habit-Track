# Import the 'os' module for operating system-related functions
import os

# Import classes for working with date and time
from datetime import datetime, date

# Import the 'sqlite3' module for SQLite database interactions
import sqlite3

# Import the 'matplotlib.pyplot' module for creating plots and graphs
import matplotlib.pyplot as plt

# Import custom User class from 'User.py'
from User import User

# Import custom Habit class from 'Habit.py'
from Habit import Habit

# Import custom HabitTracker class from 'HabitTracker.py'
from HabitTracker import HabitTracker

# Import custom Analytics class from 'Analytics.py'
from Analytics import Analytics

# Import custom StatusUpdate class from 'StatusUpdate.py'
from StatusUpdate import StatusUpdate

# Import custom Wall class from 'Wall.py'
from Wall import Wall

# Import custom HabitUpdater class from 'HabitUpdater.py'
from HabitUpdater import HabitUpdater



# Function to clear the terminal screen
def clear_screen():
    # Use 'cls' for Windows and 'clear' for other platforms
    os.system('cls' if os.name == 'nt' else 'clear')

# Function to display the main menu
def display_menu():
    # Clear the screen
    clear_screen()

    # Display the menu options
    print("\nMain Menu:")
    print("1. Log in")
    print("2. Register a new user")
    print("0. Exit")


# Function to display the user menu and handle user actions
def user_menu(user):
    while True:
        # Clear the screen
        clear_screen()

        # Display the user menu options
        print(f"Welcome back, {user.username}!")
        print("\nUser Menu:")
        print("1. Add friends")
        print("2. Post a status update")
        print("3. Create a new habit")
        print("4. Update a habit")
        print("5. Delete a habit")
        print("6. View Habits")
        print("7. View habit summary")
        print("8. View longest streak for a habit")
        print("9. View wall posts")
        print("0. Logout")

        # Get user's choice
        user_choice = input("Enter your choice: ")

        # Handle user's choice
        if user_choice == "1":
            # Add friends
            add_friends(user)

        elif user_choice == "2":
            # Post a status update
            post_status_update(user)

        elif user_choice == "3":
            # Create a new habit
            create_habit(user)

        elif user_choice == "4":
            # Update a habit
            update_habit(user)

        elif user_choice == "5":
            # Delete a habit
            delete_habit(user)

        elif user_choice == "6":
            # View habits
            view_habit_history(user)

        elif user_choice == "7":
            # View habit summary
            view_habits_summary(user)

        elif user_choice == "8":
            # View longest streak for a habit
            view_longest_streak(user)

        elif user_choice == "9":
            # View wall posts
            view_wall_posts(user)

        elif user_choice == "0":
            # Logout and return to the main menu
            break

        else:
            print("Invalid choice. Please try again.")



# Main function to run the GoalGroove application
def main():
    # Display a welcome message
    print("Welcome to GoalGroove!")

    while True:
        # Display the main menu options
        display_menu()
        
        # Get user's choice
        choice = input("Enter your choice: ")

        if choice == "1":
            # Log in
            clear_screen()
            user = login_user()
            if user:
                # Successfully logged in, display user-specific menu options
                user_menu(user)

        elif choice == "2":
            # Register a new user
            clear_screen()
            user = register_user()
            if user:
                print(f"Registration successful, welcome {user.username}!")

        elif choice == "0":
            # Exit the application
            clear_screen()
            print("Goodbye!")
            break

        else:
            clear_screen()
            print("Invalid choice. Please try again.")

        
# Function to register a new user
def register_user():
    clear_screen()
    print("User Registration")
    
    # Get user input for registration
    username = input("Enter username: ")
    email = input("Enter email: ")
    password = input("Enter password: ")
    age = int(input("Enter age: "))  # Convert age to an integer
    gender = input("Enter gender: ")

    # Create a new User object and save it to the database
    new_user = User(user_id=None, username=username, email=email, password=password, age=age, gender=gender)
    new_user.save_to_database()

# Function to log in a user
def login_user():
    clear_screen()
    print("User Login")
    
    # Get user input for login
    username = input("Enter username: ")
    password = input("Enter password: ")

    # Call the User class's login method to authenticate the user
    user = User.login(username, password)
    
    if user:
        print("Welcome back, {}!".format(user.username))
        update_all_habits_for_all_users()  # Hypothetical function call
        return user
    else:
        print("Invalid username or password.")
        input("Press Enter To Continue...")
        return None


# Function to add friends for a user
def add_friends(user):
    clear_screen()
    print("Add Friends")
    
    # Get user input for friend usernames (separated by spaces)
    friend_usernames = input("Enter friend usernames (separated by spaces): ").split()

    if friend_usernames:
        # Call the add_friends method of the User class to add friends
        user.add_friends(*friend_usernames)
        
        print("Friends added successfully!")
        print("Added friends:", ", ".join(friend_usernames))
        input("Press Enter To Continue...")
    else:
        print("No friend usernames provided.")
        input("Press Enter To Continue...")



# Function to post a status update for a user
def post_status_update(user):
    clear_screen()
    print("Post a Status Update")
    
    # Get user input for the status text
    status_text = input("Enter your status: ")
    
    # Call the post_status_update method of the User class
    user.post_status_update(status_text)
    
    print("Status update posted successfully!")
    input("Press Enter To Continue...")



# Function to check if a date string is valid
def is_valid_date(date_str):
    try:
        # Attempt to parse the date string using the specified format '%Y-%m-%d'
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        # If parsing fails, return False indicating an invalid date format
        return False


# Function to create a new habit for a user
def create_habit(user):
    clear_screen()
    print("Create a New Habit")
    
    # Get user input for habit details
    name = input("Enter habit name: ")
    description = input("Enter habit description: ")
    periodicity = input("Enter habit periodicity: ")
    
    # Get the current date in 'YYYY-MM-DD' format
    creation_date = datetime.now().strftime('%Y-%m-%d')

    while True:
        target_date_input = input("Enter habit target completion date (YYYY-MM-DD): ")
        if is_valid_date(target_date_input):
            target_completion_date = target_date_input
            break
        else:
            print("Invalid date format. Please enter the date in the format 'YYYY-MM-DD'.")

    # Create a new Habit object and save it to the database
    new_habit = Habit(user_id=user.user_id, name=name, description=description, periodicity=periodicity, creation_date=creation_date, target_completion_date=target_completion_date)
    new_habit.save_to_database()
    
    print("Habit created successfully!")

    # Function call to update habits for all users
    update_all_habits_for_all_users()



# Function to retrieve habits associated with a user
def get_user_habits(user):
    # Establish a connection to the SQLite database
    conn = sqlite3.connect('goalgroove.db')
    cursor = conn.cursor()

    # Execute a SELECT query to retrieve habits data for the given user_id
    cursor.execute('SELECT * FROM Habit WHERE user_id = ?', (user.user_id,))
    habits_data = cursor.fetchall()

    # Close the connection to the database
    conn.close()

    habits = []
    for habit_data in habits_data:
        # Create a Habit object for each retrieved habit_data
        habit = Habit(*habit_data)
        habits.append(habit)

    return habits


# Function to print details of a habit
def print_habit_details(habit):
    # Print habit details in a formatted manner
    print(f"{habit.habit_id}. {habit.name}. {habit.description} - {habit.periodicity}, {habit.creation_date}, {habit.target_completion_date}")


# Function to update a habit for a user
def update_habit(user):
    clear_screen()
    print("Update a Habit")
    
    # Get the habits associated with the user
    habits = Habit.get_habits_by_user_id(user.user_id)

    if not habits:
        print("You have no habits to update.")
        return

    print("Your Habits:")
    for habit in habits:
        print_habit_details(habit)

    habit_id_input = input("Enter the habit ID to update: ")

    # Check if the habit ID provided by the user belongs to them
    valid_habit_ids = [str(habit.habit_id) for habit in habits]
    if habit_id_input not in valid_habit_ids:
        print("Invalid habit ID. Please select a valid habit ID.")
        input("Press Enter To Continue...")
        return

    existing_habit = Habit.get_habit_by_id(habit_id_input)

    if existing_habit:
        # Get updated values from the user or keep existing values if not provided
        name = input(f"Enter updated habit name [{existing_habit.name}]: ")
        description = input(f"Enter updated habit description [{existing_habit.description}]: ")
        periodicity = input(f"Enter updated habit periodicity [{existing_habit.periodicity}]: ")
        target_completion_date = input(f"Enter updated habit target completion date (YYYY-MM-DD) [{existing_habit.target_completion_date}]: ")

        # Update the habit's attributes with the provided values or keep existing values
        existing_habit.name = name if name else existing_habit.name
        existing_habit.description = description if description else existing_habit.description
        existing_habit.periodicity = periodicity if periodicity else existing_habit.periodicity
        existing_habit.target_completion_date = target_completion_date if target_completion_date else existing_habit.target_completion_date

        # Update the habit in the database
        existing_habit.update_habit()
        print("Habit updated successfully!")
    else:
        print("Habit not found or you do not have permission to update this habit.")
    
    # Hypothetical function call to update habits for all users
    update_all_habits_for_all_users()

    input("Press Enter To Continue...")



# Function to view habit history for a user
def view_habit_history(user):
    clear_screen()
    print("View Habit History")

    # Get all habits for the user
    habits = Habit.get_habits_by_user_id(user.user_id)

    if not habits:
        print("You have no habits to view.")
        return

    # Display the list of habits with headings
    print("{:<5} {:<20} {:<40} {:<20} {:<15} {:<15}".format(
        "ID", "Habit Name", "Description", "Periodicity", "Creation Date", "Target Completion Date"
    ))
    print("="*126)
    for habit in habits:
        print("{:<5} {:<20} {:<40} {:<20} {:<15} {:<15}".format(
            habit.habit_id, habit.name, habit.description, habit.periodicity, 
            habit.creation_date, habit.target_completion_date
        ))

    input("Press Enter To Continue...")



# Function to view habits summary for a user
def view_habits_summary(user):
    clear_screen()
    print("Plotting Completion Percentage for Habits")
    
    # Create a HabitTracker instance for the user and plot completion percentage
    habit_tracker = HabitTracker(user.user_id)
    habit_tracker.plot_completion_percentage()

    input("Press Enter To Continue...")


# Function to view the longest streak for all habits of a user
def view_longest_streak(user):
    clear_screen()
    print("View Longest Streak for All Habits")

    # Create an Analytics instance for the user and get longest streaks
    analytics = Analytics(user.user_id)
    habit_streaks = analytics.get_longest_streak()

    if habit_streaks:
        print("Longest Streaks for All Habits:")
        habits = list(habit_streaks.keys())
        streak_lengths = list(habit_streaks.values())

        # Create a bar plot with habit names and their streak lengths
        plt.bar(habits, streak_lengths, color='skyblue')

        plt.xlabel('Habit Name')
        plt.ylabel('Streak Length (Days)')
        plt.title('Longest Streak for All Habits')
        plt.xticks(rotation=45, ha='right')

        # Add annotations for the streak lengths on top of the bars
        for i, streak in enumerate(streak_lengths):
            plt.text(i, streak, str(streak), ha='center', va='bottom')

        # Add grid lines
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        # Display the plot
        plt.tight_layout()
        plt.show()
    else:
        print("No habits found or no streaks available.")

    input("Press Enter To Continue...")


# Function to view wall posts (status updates) for a user
def view_wall_posts(user):
    clear_screen()
    print("View Status Updates")

    # Create a Wall instance for the user and get wall posts
    wall = Wall(user.user_id)
    wall_posts = wall.get_wall_posts()

    if wall_posts:
        print("Wall Posts:")
        for post in wall_posts:
            print(f"{post['username']} - {post['timestamp']}")
            print(post['text'])
            print()

    else:
        print("No status updates found.")
    
    input("Press Enter To Continue...")



# Function to delete a habit for a user
def delete_habit(user):
    clear_screen()
    print("Delete a Habit")

    # Get the user's habits
    habits = Habit.get_habits_by_user_id(user.user_id)

    if not habits:
        print("You have no habits to delete.")
        input("Press Enter To Continue...")
        return

    # Display the user's habits
    print("Your Habits:")
    for habit in habits:
        print_habit_details(habit)

    habit_id_input = input("Enter the habit ID to delete: ")

    # Get the habit by ID
    habit_to_delete = Habit.get_habit_by_id(habit_id_input)

    if habit_to_delete:
        # Delete the habit from the database
        habit_to_delete.delete_habit()
        print("Habit deleted successfully!")
    else:
        print("Habit not found.")

    input("Press Enter To Continue...")


# Function to update goal periods for all habits of all users
def update_all_habits_for_all_users():
    # Get all users
    users = User.get_all_users()

    # Iterate through each user
    for user in users:
        # Create a HabitUpdater instance for the user
        updater = HabitUpdater(user.user_id)

        # Get the user's habits
        habits = Habit.get_habits_by_user_id(user.user_id)

        # Update goal periods for the user's habits
        updater.update_goal_periods(habits)


if __name__ == "__main__":
    update_all_habits_for_all_users()
    main()

