import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

class Task:
    def __init__(self, username = None, title = None, description = None, due_date = None, assigned_date = None, completed = None, task_number = None):
        '''
        Inputs:
        username: String
        title: String
        description: String
        due_date: DateTime
        assigned_date: DateTime
        completed: Boolean
        task_number: Integer
        '''
        self.username = username
        self.title = title
        self.description = description
        self.due_date = due_date
        self.assigned_date = assigned_date
        self.completed = completed
        self.task_number = task_number

    def from_string(self, task_str):
        '''
        Convert from string in tasks.txt to object
        '''
        tasks = task_str.split(";")
        username = tasks[0]
        title = tasks[1]
        description = tasks[2]
        due_date = datetime.strptime(tasks[3], DATETIME_STRING_FORMAT)
        assigned_date = datetime.strptime(tasks[4], DATETIME_STRING_FORMAT)
        completed = True if tasks[5] == "Yes" else False
        task_number = tasks[6]
        self.__init__(username, title, description, due_date, assigned_date, completed, task_number)


    def to_string(self):
        '''
        Convert to string for storage in tasks.txt
        '''
        str_attrs = [
            self.username,
            self.title,
            self.description,
            self.due_date.strftime(DATETIME_STRING_FORMAT),
            self.assigned_date.strftime(DATETIME_STRING_FORMAT),
            "Yes" if self.completed else "No",
            self.task_number
        ]
        return ";".join(str_attrs)

    def display(self):
        '''
        Display object in readable format
        '''
        disp_str = f"Task number: \t {self.task_number}\n" 
        disp_str += f"Task: \t\t {self.title}\n"
        disp_str += f"Assigned to: \t {self.username}\n"
        disp_str += f"Date Assigned: \t {self.assigned_date.strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {self.due_date.strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n{self.description}\n"
        return disp_str
        

# Read and parse tasks.txt
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]


task_list = []
for t_str in task_data:
    curr_t = Task()
    curr_t.from_string(t_str)
    task_list.append(curr_t)

# Read and parse user.txt

# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

# Keep trying until a successful login
logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True

def validate_string(input_str):
    '''
    Function for ensuring that string is safe to store
    '''
    if ";" in input_str:
        print("Your input cannot contain a ';' character")
        return False
    return True

def check_username_and_password(username, password):
    '''
    Ensures that usernames and passwords can't break the system
    '''
    # ';' character cannot be in the username or password
    if ";" in username or ";" in password:
        print("Username or password cannot contain ';'.")
        return False
    return True

def write_usernames_to_file(username_dict):
    '''
    Function to write username to file

    Input: dictionary of username-password key-value pairs
    '''
    with open("user.txt", "w") as out_file:
        user_data = []
        for k in username_dict:
            user_data.append(f"{k};{username_dict[k]}")
        out_file.write("\n".join(user_data))

def reg_user():
    
    # Request input of a new username
    new_username = input("New Username: ")
    
    # Prevents duplication of usernames
    while new_username in username_password:
        print("Username already exists. Enter a new username.")
        new_username = input("New Username: ")

    # Request input of new password    
    new_password = input("New Password: ")

    # Validates username and password to ensure system does not break
    while check_username_and_password(new_username, new_password) == False:
        # Request input of a new username and password
        new_username = input("New Username: ")
        
        new_password = input("New Password: ")
        

    # Request input of password confirmation
    confirm_password = input("Confirm Password: ")

    # Check if the new password and confirmed password are the same.
    if new_password == confirm_password:
        # If they are the same, add them to the user.txt file,
        print("New user added")

        # Add to dictionary and write to file
        username_password[new_username] = new_password
        write_usernames_to_file(username_password)

        # Otherwise you present a relevant message
    else:
        print("Passwords do no match. Please try registering the user from the menu again.")

def add_task():
    # Add a new task
    # Prompt a user for the following: 
    #     A username of the person whom the task is assigned to,
    #     A title of a task,
    #     A description of the task and 
    #     the due date of the task.

    # Ask for username
    task_username = input("Name of person assigned to task: ")
    if task_username not in username_password.keys():
        print("User does not exist. Please enter a valid username")
        task_username = input("Name of person assigned to task: ")
    
    # Assigns a task number to the task
    with open("tasks.txt", 'r') as task_file:
        task_data = task_file.read().split("\n")
        task_data = [t for t in task_data if t != ""]
    task_number = str(len(task_data))
    print(f"Task number: {task_number}")
    

    # Get title of task and ensure safe for storage
    while True:
        task_title = input("Title of Task: ")
        if validate_string(task_title):
            break

    # Get description of task and ensure safe for storage
    while True:
        task_description = input("Description of Task: ")
        if validate_string(task_description):
            break

    # Obtain and parse due date
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break
        except ValueError:
            print("Invalid datetime format. Please use the format specified")
    
    # Obtain and parse current date
    curr_date = date.today()
        
    # Create a new Task object and append to list of tasks
    new_task = Task(task_username, task_title, task_description, due_date_time,curr_date, False, task_number)
    task_list.append(new_task)

    # Write to tasks.txt
    with open("tasks.txt", "w") as task_file:
        task_file.write("\n".join([t.to_string() for t in task_list]))
    print("Task successfully added.")

def view_all():
    print("-----------------------------------")

    if len(task_list) == 0:
        print("There are no tasks.")
        print("-----------------------------------")

    for t in task_list:
        print(t.display())
        print("-----------------------------------")

def view_mine(task_list, curr_user):
    print("-----------------------------------")
    has_task = False
    for t in task_list:
        if t.username == curr_user:
            has_task = True
            print(t.display())
            print("-----------------------------------")

    # Gives option to select a task to edit or mark complete
    print("Select a task by typing in it's corresponding number or return to the menu by entering '-1'.")
    selected_task = int(input("Task number: "))
    
    # Keep asking for input until asked to return to main menu (entering '-1')
    while selected_task != -1:

        # Provides options to edit task or mark complete
        choice = input("Select one of the following:\nd - Edit task\nmc - Mark task as complete\ne - Exit to Task Number\n: ").lower()
        
        # Opens task.txt file containing tasks to read
        with open("tasks.txt", "r+") as task_file:
            task_data = task_file.read().split("\n")
            
            task_data = [t for t in task_data if t != ""]
            
            
            # Marks task as complete
            if choice == "mc":
                task_data1 = task_data[selected_task].split(";")
                task_data1[5] = "Yes"
                task_data[selected_task] = ";".join(task_data1)
                task_data = "\n".join(task_data)
                # Writes changes to "tasks.txt"
                with open("tasks.txt", "w") as task_file:
                    task_file.write(f"{task_data}")
            
            elif choice == "e":
                break
            
            # Allows user to edit selected task
            elif choice == "d":
                task_data1 = task_data[selected_task].split(";")
                # Allows changes if task is not complete.
                if task_data1[5] == "No":
                    # Changes who the task is assigned to.
                    new_task_username = input("Name of person assigned to task: ")
                    validate_string(new_task_username)

                    if new_task_username not in username_password.keys():
                        print("User does not exist. Please enter a valid username")
                        new_task_username = input("Name of person assigned to task: ")
                        validate_string(new_task_username)
                    task_data1[0] = new_task_username

                    # Changes due date
                    new_task_due_date = input("Due date of task (YYYY-MM-DD): ")
                    try:
                        datetime.strptime(new_task_due_date, DATETIME_STRING_FORMAT)
                    except ValueError:
                        raise ValueError("Incorrect data format, should be YYYY-MM-DD")

                    task_data1[3] = new_task_due_date
                    task_data[selected_task] = ";".join(task_data1)
                    task_data = "\n".join(task_data)
                    
                    # Outputs changes to tasks.txt
                    with open("tasks.txt", "w") as task_file:
                        task_file.write(f"{task_data}")
                
                # Tasks cannot be edited if complete.
                else:
                    print("Task has been completed. You cannot edit a completed task.")
            
            # If user does not enter a recognised input
            else:
                print("Please select a valid option.")

            ##elif choice == "d": strings = [str(i) for i in string_list]

        selected_task = input("Task number ('-1' to return to menu): ")


    if not has_task:
        print("You have no tasks.")
        print("-----------------------------------")

def percentage(x, total):
    percent = (x/total) * 100
    return percent

def indices(lst, item):
    return [i for i, x in enumerate(lst) if x == item]    

def generate_report():
    # Read task data to generate report
        with open("tasks.txt", "r") as task_file:
            task_data = task_file.read().split("\n")
            
#####TASK_OVERVIEW.TXT#####
            # Initial report values
            overdue = 0 # Incomplete and after due date
            before_due = 0 # Incomplete and before due date
            completed = 0 # Completed
            completion_status = [] #"i"=incomplete, "o"=overdue and incomplete, "c"=completed

            # Today's date as reference as to whether overdue
            current_date = str(date.today()).split("-")
            
            # Check task due dates & status of completion for tasks
            for idx in range(0, len(task_data)):
                task_due_date = task_data[idx].split(";")

                # Check uncompleted&/overdue tasks due dates
                if task_due_date[5] == "No":
                
                    task_due_date = task_due_date[3].split("-")

                    if int(task_due_date[0]) > int(current_date[0]):
                        before_due += 1
                        completion_status.append("i")

                    elif int(task_due_date[0]) == int(current_date[0]):

                        if int(task_due_date[1]) > int(current_date[1]):
                            before_due += 1
                            completion_status.append("i")

                    elif int(task_due_date[1]) == int(current_date[1]):

                        if int(task_due_date[2]) >= int(current_date[2]):
                            before_due += 1
                            completion_status.append("i")

                        else:
                            overdue += 1
                            completion_status.append("o")

                    else:
                        overdue += 1
                        completion_status.append("o")

                # Check number of completed tasks
                elif task_due_date[5] == "Yes":
                    completed += 1
                    completion_status.append("c")
            # Calculate number of uncompleted tasks and total number of tasks        
            uncompleted = overdue + before_due
            total_num_tasks = uncompleted + completed

            # To see list of completion_status: print(completion_status)

            # Percentages
            incomp_percent = percentage(uncompleted, total_num_tasks)
            od_percent = percentage(overdue, total_num_tasks)
        
        # Store results in readable format in "task_overview.txt"
        with open("task_overview.txt", "w") as t_o_file:
            t_o_file.write(f"""The following information generated and tracked by task_manager.py.\n
Total number of tasks: \t\t\t\t {total_num_tasks}
Total number of completed tasks: \t\t {completed}
Total number of uncompleted tasks: \t\t {uncompleted}
Number of incomplete and overdue tasks: \t {overdue}
Percentage of incomplete tasks: \t\t {incomp_percent}%
Percentage of overdue tasks: \t\t\t {od_percent}%""")
            
####USER_OVERVIEW.TXT####
        # Opens user information from text file
        with open("user.txt", 'r') as user_file:
            user_data = user_file.read().split("\n")
            # Determines the total number of users registered on task_manager.py
            total_num_users = len(user_data)

            # Creates a list of users and their passwords registered
            read_user_data = []
            for index in range(0, len(user_data)):
                read_user_data += user_data[index].split(";")

            # Creates a list of users only
            users = []
            for indx in range(0, len(read_user_data)):
    
                if indx % 2 == 0:
                    users.append(read_user_data[indx])
            
            # Writes results in a readable format in "user_overview.txt"
            with open("user_overview.txt", "w") as u_o_file:
                u_o_file.write(f"""The following information has been generated and tracked by task_manager.py.
Total number of registered users: {len(users)}
Total number of registered tasks: {total_num_tasks}\n""")

        users_assigned_tasks = []
        
        # opens file containing task data to read
        with open("tasks.txt", "r") as task_file:
            # make a list of the users assigned to tasks
            for line in task_file:
                users_assigned_tasks.append(line.split(";")[0])

            # Creates a dictionary that assigns each user to the index of their task status
            for name in users:
                dictionary = dict((name, indices(users_assigned_tasks, name)) for name in set(users_assigned_tasks) if users_assigned_tasks.count(name) > 0)

            for i in range(len(users)):
                num_tasks_assigned = users_assigned_tasks.count(users[i])
                percentage_tasks_to_user = percentage(num_tasks_assigned, len(users_assigned_tasks))
                # Appends to "user_overview.txt"
                with open("user_overview.txt", "a") as u_o_file:
                    u_o_file.write(f"""
{users[i]} assigned to {percentage_tasks_to_user}% of tasks that have been assigned in total.""")
            
            # Determines the numbers and percentages for each user to be stored in 'user_overview.txt'
            for u in users:
                counter = f"{u}:"
    
                for i in range(len(dictionary[u])):
                    counter += completion_status[dictionary.__getitem__(u)[i]]
                    complete = counter.split(":")[1].count("c")
                    incomplete = counter.split(":")[1].count("i")
                    overdue = counter.split(":")[1].count("o")
                    uncomplete = incomplete + overdue
                    total_to_user = complete + incomplete + overdue
                # Appends to "user_overview.txt"
                with open("user_overview.txt", "a") as u_o_file:
                    u_o_file.write(f"""\n\n{u} assigned to {total_to_user} tasks
{u} completed {percentage(complete, total_to_user)}% of their tasks
{u} has yet to complete {percentage(uncomplete, total_to_user)}% of their tasks
Percentage of tasks assigned to {u} overdue: {percentage(overdue, total_to_user)}%""")

#########################
# Main Program
######################### 

while True:
    # Get input from user
    print()
    if curr_user == 'admin':
        menu = input('''Select one of the following Options below:
                        r - Registering a user
                        a - Adding a task
                        va - View all tasks
                        vm - View my task
                        gr - Generate report
                        ds - Display statistics
                        e - Exit
                        : ''').lower()
    else:
        menu = input('''Select one of the following Options below:
                        r - Registering a user
                        a - Adding a task
                        va - View all tasks
                        vm - View my tasks
                        e - Exit
                        : ''').lower()

    if menu == 'r': # Register new user (if admin)

        if curr_user != 'admin':
            print("Registering new users requires admin privileges")
            continue
        if curr_user == 'admin':
            reg_user()

    elif menu == 'a': # Add a new task
        add_task()

    elif menu == 'va': # View all tasks
        view_all()

    elif menu == 'vm': # View my tasks
        view_mine(task_list, curr_user)

    elif menu == 'gr' and curr_user == 'admin': # If admin, generate reports
        
        generate_report()
        print("Reports have been generated.")

    elif menu == 'ds' and curr_user == 'admin': # If admin, display statistics
        generate_report()
        print("Statistics:\n")
        # Opens "task_overview.txt" to read
        with open("task_overview.txt", "r") as t_overview:
            task_overview = t_overview.read()
            print(task_overview) # prints task_overview.txt's info
            print("\n")
        with open("user_overview.txt", "r") as u_overview:
            user_overview = u_overview.read()
            print(user_overview) # prints user_overview.txt's info

    elif menu == 'e': # Exit program
        print('Goodbye!!!')
        exit()

    else: # Default case
        print("You have made a wrong choice, Please Try again")