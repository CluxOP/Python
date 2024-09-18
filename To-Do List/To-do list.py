import tabulate, time

to_dos = [["Title", "Description", "Value"]]

def check_input(input):

    '''
    Returns True if the given input is valid else False
    '''

    if input in ["A", "C", "V", "D", "Q"]:
        return True
    
    return False


def auto_delete_completed():
    '''
    Automatically deletes all to-dos marked as completed
    '''
    # Iterated through all todo in to_dos list
    for todo in to_dos:
        # Pop todo if it is marked as Completed
        if todo[-1] == "Completed":
            to_dos.pop(to_dos.index(todo))


def add_todo():
    '''
    Add to-do to the to_dos list
    '''
    # Ask the user for a title and description
    try:
        title = input("Please provide a title: ")
        desc = input("Please provide a description: ")
    except EOFError:
        return

    # Add the task to a global variable
    to_dos.append([title, desc, "Pending"])

    print("A new to-do added!")

    time.sleep(2)


def update_todo():
    '''
    Updates the value of to-do to be pending or completed
    '''
    # Print all to-dos
    print(tabulate.tabulate(to_dos, showindex=True , tablefmt="rounded_outline"))

    while True:
        try:
            # Ask the user for a todo to update
            todo_to_update = input("Which to-do you want to update: ")

            # Check if the to-do is available or not
            if int(todo_to_update) > len(to_dos) - 1 or int(todo_to_update) == 0:
                print(f"There is no to-do no.{todo_to_update} to update. Please provide a valid to-do no.")
                continue
            else:
                # Update the value of to-do
                to_dos[int(todo_to_update)][-1] = "Completed"

                print("To-do updated!")
                break

        except ValueError:
            print("Enter valid to-do to update")
            continue

        except EOFError:
            return

    time.sleep(2)


def view_todo():
    '''
    Print all current to-dos
    '''
    print(tabulate.tabulate(to_dos, showindex=True , tablefmt="rounded_outline"))

    time.sleep(2)


def delete_todo():
    '''
    Deletes todo from the to_dos list
    '''
    # Print all to-dos
    print(tabulate.tabulate(to_dos, showindex=True , tablefmt="rounded_outline"))

    while True:
        try:
            # Ask the user for a todo to delete
            todo_to_delete = input("Which to-do you want to delete: ")

            # Check if the to-do is available or not
            if int(todo_to_delete) > len(to_dos) - 1 or int(todo_to_delete) == 0:
                print(f"There is no to-do no.{todo_to_delete} to delete :( Please provide a valid to-do no.")
                continue
            else:
                # Update the value of to-do
                to_dos.pop(int(todo_to_delete))

                print("To-do deleted!")
                break

        except ValueError:
            print("Enter valid to-do to delete")
            continue

        except EOFError:
            return

    time.sleep(2)

def main():

    # Make an infinite loop to take user inputs
    while True:

        # Print a table of available task
        print(tabulate.tabulate({
            "Sr No.": [1, 2, 3, 4, 5],
            "Operation": ["Add a new to-do", "Update a to-do as complete", "View all to-dos", "Delete a to-do", "Quit"],
            "Key": ["A", "C", "V", "D", "Q"]
        }, headers="keys", tablefmt="rounded_outline"))

        # Ask the user for an input and exit if user inputed Ctrl + Z
        try:
            user_input = input("Choose an operation to-do: ").upper()
        except EOFError:
            break

        # Delete completed todo
        auto_delete_completed()

        # Check the user input
        if check_input(user_input):
            # Handle inputs
            if user_input == "A":
                add_todo()
            elif user_input == "C" and len(to_dos) != 1:
                update_todo()
            elif user_input == "V" and len(to_dos) != 1:
                view_todo()
            elif user_input == "D" and len(to_dos) != 1:
                delete_todo()
            elif user_input == "Q":
                break
            else:
                print("Its All Empty here! Add a to-do first :)")
                time.sleep(2)
        else:
            print("Please enter a valid key")
            time.sleep(2)
            


if __name__ == "__main__":
    main()