

import datetime
import os



# Read the existing data from the file
with open("tasks.txt", "r") as file:
    existing_data = file.read()

# Split the existing data into individual tasks
existing_tasks = existing_data.split("\n\n")

# Remove any empty tasks (in case there are extra empty lines at the end)
existing_tasks = [task for task in existing_tasks if task.strip()]

# Process each task to convert it to the desired format
formatted_tasks = []
for task in existing_tasks:
    task_data = task.split(";")
    formatted_task = ";".join(task_data).strip(";")
    formatted_tasks.append(formatted_task)

# Write the formatted tasks back to the file
with open("tasks.txt", "w") as file:
    file.write("\n".join(formatted_tasks))






# Function to check if a date is in the correct format
def is_valid_date(date_str):
    try:
        datetime.datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False
def login():
    # Read user credentials from user.txt
    with open("user.txt", "r") as user_file:
        users = [line.strip().split(";") for line in user_file]

    while True:
        username = input("Username: ")
        password = input("Password: ")

        for user in users:
            if user[0] == username and user[1] == password:
                print("Login successful!\n")
                return username

        print("Invalid username or password. Please try again.\n")







def reg_user(): # Function to register a new user
    new_username = input("New Username: ")
    # Check if the username already exists in user.txt
    with open("user.txt", "r") as user_file:
        existing_usernames = [line.split(";")[0] for line in user_file.readlines()]

    if new_username in existing_usernames:
        print("Username already exists. Please choose a different username.")
        return

    new_password = input("New Password: ")
    confirm_password = input("Confirm Password: ")

    if new_password == confirm_password:
        print("New user added")
        with open("user.txt", "a") as user_file:
            user_file.write(f"{new_username};{new_password}\n")
    else:
        print("Passwords do not match")


def add_task():
    task_username = input("Assignee Username: ")
    task_title = input("Task Title: ")
    task_description = input("Task Description: ")
    task_due_date = input("Due Date (YYYY-MM-DD): ")
    task_completed = "No"

    # Write the new task's data to tasks.txt with the correct format and delimiter
    with open("tasks.txt", "a") as task_file:
        task_file.write(f"{task_username};{task_title};{task_description};{task_due_date};{task_completed}\n")

    print("Task added successfully!")



def view_all():
    with open("tasks.txt", "r") as task_file:
        tasks = task_file.readlines()

    if len(tasks) == 0:
        print("No tasks found.")
        return

    print("All tasks:")
    for index, task in enumerate(tasks, start=1):
        task_data = task.strip().split(";")
        print(f"Task {index}:")
        print(f"Assigned to: {task_data[0]}")
        print(f"Title: {task_data[1]}")
        print(f"Description: {task_data[2]}")
        print(f"Due Date: {task_data[3]}")
        print(f"Task Complete? {task_data[4]}")
        print()


def view_mine(curr_user):
    username = curr_user

    with open("tasks.txt", "r") as task_file:
        tasks = task_file.readlines()

    user_tasks = []
    for task in tasks:
        task_data = task.strip().split(";")
        if task_data[0] == username:
            user_tasks.append(task_data)

    if len(user_tasks) == 0:
        print("No tasks found for the user.")
        return

    print(f"Tasks assigned to {username}:")
    for index, task_data in enumerate(user_tasks, start=1):
        print(f"Task {index}:")
        print(f"Title: {task_data[1]}")
        print(f"Description: {task_data[2]}")
        print(f"Due Date: {task_data[3]}")
        print(f"Task Complete? {task_data[4]}")
        print()

    while True:
        choice = input("Enter the number of the task you want to perform an action on (or 'q' to quit): ")

        if choice.lower() == "q":
            break

        if choice.isdigit():
            task_index = int(choice) - 1
            if 0 <= task_index < len(user_tasks):
                selected_task = user_tasks[task_index]
                print("Selected Task:")
                print(f"Title: {selected_task[1]}")
                print(f"Description: {selected_task[2]}")
                print(f"Due Date: {selected_task[3]}")
                print(f"Task Complete? {selected_task[4]}")

                action_choice = input("Select an action: (c - mark as complete, e - edit, q - quit) ")
                if action_choice.lower() == "c":
                    selected_task[4] = "Yes"
                elif action_choice.lower() == "e":
                    new_title = input("Enter the new Task Title: ")
                    new_description = input("Enter the new Task Description: ")
                    new_due_date = input("Enter the new Due Date (YYYY-MM-DD): ")
                    selected_task[1] = new_title
                    selected_task[2] = new_description
                    selected_task[3] = new_due_date
                elif action_choice.lower() == "q":
                    break
                else:
                    print("Invalid choice. Please try again.")
            else:
                print("Invalid task number. Please try again.")
        else:
            print("Invalid input. Please enter a number or 'q' to quit.")

    # Write the updated tasks back to the file
    updated_tasks = []
    for task_data in tasks:
        for user_task in user_tasks:
            if user_task[1] == task_data.split(";")[1]:  # Check for matching task titles
                task_data = ";".join(user_task)
                break
        updated_tasks.append(task_data)

    # Write the updated tasks back to the file
    with open("tasks.txt", "w") as task_file:
        task_file.write("\n".join(formatted_tasks))

    print("Task(s) updated successfully!")






def mark_task_complete():
    task_id = input("Enter the Task ID to mark as complete: ")

    # Read all tasks from tasks.txt
    with open("tasks.txt", "r") as task_file:
        tasks = task_file.readlines()

    task_found = False
    updated_tasks = []
    for task in tasks:
        task_data = task.strip().split(";")
        if task_data[4] == "No" and task_data[0] == curr_user:
            if task_id == str(task_data[1]):
                task_data[4] = "Yes"
                task_found = True
        updated_tasks.append(",".join(task_data))

    if not task_found:
        print("Task not found or cannot be marked as complete.")
        return

    # Write the updated tasks back to tasks.txt
    with open("tasks.txt", "w") as task_file:
        task_file.write("\n".join(updated_tasks))

    print("Task marked as complete successfully!")


def edit_task():
    task_id = input("Enter the Task ID to edit: ")

    # Read all tasks from tasks.txt
    with open("tasks.txt", "r") as task_file:
        tasks = task_file.readlines()

    task_found = False
    updated_tasks = []
    for task in tasks:
        task_data = task.strip().split(";")
        if task_data[0] == curr_user:
            if task_id == str(task_data[1]):
                if task_data[4] == "Yes":
                    print("Task has already been completed. Cannot edit.")
                    return
                else:
                    task_title = input("New Task Title: ")
                    task_description = input("New Task Description: ")
                    task_due_date = input("New Due Date (YYYY-MM-DD): ")
                    task_data[1] = task_title
                    task_data[2] = task_description
                    task_data[3] = task_due_date
                    task_found = True
        updated_tasks.append(",".join(task_data))

    if not task_found:
        print("Task not found or cannot be edited.")
        return

    # Write the updated tasks back to tasks.txt
    with open("tasks.txt", "w") as task_file:
        task_file.write("\n".join(updated_tasks))

    print("Task edited successfully!")


def generate_reports(curr_user):
    # Read all tasks from tasks.txt
    with open("tasks.txt", "r") as task_file:
        tasks = task_file.readlines()

    total_tasks = len(tasks)
    completed_tasks = 0
    overdue_tasks = 0

    today_date = datetime.date.today()

    for task in tasks:
        task_data = task.strip().split(";")
        if len(task_data) == 5:  # Ensure that the task data has the expected number of elements
            if task_data[4].lower() == "yes":
                completed_tasks += 1
            else:
                if is_valid_date(task_data[3]):
                    due_date = datetime.datetime.strptime(task_data[3], '%Y-%m-%d').date()
                    if due_date < today_date:
                        overdue_tasks += 1

    pending_tasks = total_tasks - completed_tasks - overdue_tasks

    # Calculate the percentage of completed tasks
    if total_tasks > 0:
        completed_task_percentage = (completed_tasks / total_tasks) * 100
    else:
        completed_task_percentage = 0

    # Save the statistics to files
    with open("task_overview.txt", "w") as task_overview_file:
        task_overview_file.write(f"Total Tasks: {total_tasks}\n")
        task_overview_file.write(f"Completed Tasks: {completed_tasks}\n")
        task_overview_file.write(f"Overdue Tasks: {overdue_tasks}\n")
        task_overview_file.write(f"Pending Tasks: {pending_tasks}\n")
        task_overview_file.write(f"Completed Task Percentage: {completed_task_percentage:.2f}%")

    with open("user_overview.txt", "w") as user_overview_file:
        user_overview_file.write(f"Username: {curr_user}\n")  # Use 'curr_user' variable
        user_overview_file.write(f"Total Tasks: {total_tasks}\n")
        user_overview_file.write(f"Completed Tasks: {completed_tasks}\n")
        user_overview_file.write(f"Overdue Tasks: {overdue_tasks}\n")
        user_overview_file.write(f"Pending Tasks: {pending_tasks}\n")
        user_overview_file.write(f"Completed Task Percentage: {completed_task_percentage:.2f}%")

    print("Task Overview:")
    print(f"Total Tasks: {total_tasks}")
    print(f"Completed Tasks: {completed_tasks}")
    print(f"Overdue Tasks: {overdue_tasks}")
    print(f"Pending Tasks: {pending_tasks}")
    print(f"Completed Task Percentage: {completed_task_percentage:.2f}%")







def display_statistics():
    with open("task_overview.txt", "r") as task_overview_file:
        task_overview = task_overview_file.read()

    with open("user_overview.txt", "r") as user_overview_file:
        user_overview = user_overview_file.read()

    print("Task Statistics:")
    print(task_overview)
    print()
    print("User Statistics:")
    print(user_overview)





def main():
    os.system("cls" if os.name == "nt" else "clear")
    print("Task Manager")
    print("-------------")

    curr_user = login()  # Log in and get the current user's username

    while True:
        print("Please select one of the following options:")
        print("r  - Register user")
        print("a  - Add task")
        print("va - View all tasks")
        print("vm - View my tasks")
        print("gr - Generate reports")
        print("ds - Display statistics")
        print("e  - Exit")

        choice = input("Enter your choice: ")

        if choice == "r":
            reg_user()
        elif choice == "a":
            add_task()
        elif choice == "va":
            view_all()
        elif choice == "vm":
            view_mine(curr_user)  # Pass 'curr_user' to the function call

        elif choice == "gr":
            generate_reports(curr_user)  # Pass 'curr_user' to the function call

        elif choice == "ds":
            display_statistics()
        elif choice == "e":
            print("Exiting Task Manager. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.\n")

if __name__ == "__main__":
    main()