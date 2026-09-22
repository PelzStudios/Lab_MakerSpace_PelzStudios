from database import initialize_database
from services import (
    register_member,
    list_members,
    update_member,
    register_equipment,
    list_equipment,
    update_equipment,
    create_loan,
    return_loan,
    search_members,
    search_equipment,
    list_active_loans,
    report_overdue_loans,
    report_equipment_by_category,
    report_member_loan_history,
)


def get_int(prompt):
    """Keep asking until the user enters a whole number."""
    while True:
        value = input(prompt).strip()

        try:
            return int(value)
        except ValueError:
            print("Error: Please enter a valid number.")


def pause():
    input("\nPress Enter to continue...")


def member_menu():
    while True:
        print("\n--- MEMBERS ---")
        print("1. Register member")
        print("2. List members")
        print("3. Update member")
        print("0. Back")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            name = input("Name: ").strip()
            email = input("Email: ").strip()
            phone = input("Phone: ").strip()

            try:
                member_id = register_member(name, email, phone)
                print(f"Member registered successfully. ID: {member_id}")
            except ValueError as error:
                print(f"Error: {error}")
            pause()

        elif choice == "2":
            list_members()
            pause()

        elif choice == "3":
            member_id = get_int("Member ID: ")
            name = input("New name: ").strip()
            email = input("New email: ").strip()
            phone = input("New phone: ").strip()

            try:
                if update_member(member_id, name, email, phone):
                    print("Member updated successfully.")
                else:
                    print("Error: Member not found.")
            except ValueError as error:
                print(f"Error: {error}")
            pause()

        elif choice == "0":
            return

        else:
            print("Invalid choice.")


def equipment_menu():
    while True:
        print("\n--- EQUIPMENT ---")
        print("1. Register equipment")
        print("2. List equipment")
        print("3. Update equipment")
        print("0. Back")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            name = input("Equipment name: ").strip()
            category = input("Category: ").strip()

            try:
                equipment_id = register_equipment(name, category)
                print(f"Equipment registered successfully. ID: {equipment_id}")
            except ValueError as error:
                print(f"Error: {error}")
            pause()

        elif choice == "2":
            list_equipment()
            pause()

        elif choice == "3":
            equipment_id = get_int("Equipment ID: ")
            name = input("New name: ").strip()
            category = input("New category: ").strip()

            print("1. Available")
            print("2. Maintenance")
            status_choice = input("Status: ").strip()

            if status_choice == "1":
                status = "available"
            elif status_choice == "2":
                status = "maintenance"
            else:
                print("Invalid status.")
                pause()
                continue

            try:
                if update_equipment(equipment_id, name, category, status):
                    print("Equipment updated successfully.")
                else:
                    print("Error: Equipment not found.")
            except ValueError as error:
                print(f"Error: {error}")
            pause()

        elif choice == "0":
            return

        else:
            print("Invalid choice.")


def loan_menu():
    while True:
        print("\n--- LOANS ---")
        print("1. Checkout equipment")
        print("2. Return equipment")
        print("3. List active loans")
        print("0. Back")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            member_id = get_int("Member ID: ")
            equipment_id = get_int("Equipment ID: ")
            due_date = input("Due date (YYYY-MM-DD): ").strip()

            try:
                loan_id = create_loan(member_id, equipment_id, due_date)
                print(f"Loan created successfully. Loan ID: {loan_id}")
            except ValueError as error:
                print(f"Error: {error}")
            pause()

        elif choice == "2":
            loan_id = get_int("Loan ID: ")

            try:
                if return_loan(loan_id):
                    print("Equipment returned successfully.")
                else:
                    print("Error: Active loan not found.")
            except ValueError as error:
                print(f"Error: {error}")
            pause()

        elif choice == "3":
            list_active_loans()
            pause()

        elif choice == "0":
            return

        else:
            print("Invalid choice.")


def search_menu():
    while True:
        print("\n--- SEARCH ---")
        print("1. Search member")
        print("2. Search equipment")
        print("0. Back")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            term = input("Enter member name or ID: ").strip()
            search_members(term)
            pause()

        elif choice == "2":
            term = input("Enter equipment name or ID: ").strip()
            search_equipment(term)
            pause()

        elif choice == "0":
            return

        else:
            print("Invalid choice.")


def reports_menu():
    while True:
        print("\n--- REPORTS ---")
        print("1. Currently borrowed equipment")
        print("2. Overdue loans")
        print("3. Equipment by category")
        print("4. Member loan history")
        print("0. Back")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            list_active_loans()
            pause()

        elif choice == "2":
            report_overdue_loans()
            pause()

        elif choice == "3":
            report_equipment_by_category()
            pause()

        elif choice == "4":
            member_id = get_int("Member ID: ")
            report_member_loan_history(member_id)
            pause()

        elif choice == "0":
            return

        else:
            print("Invalid choice.")


def main():
    initialize_database()

    while True:
        print("\n================================")
        print("     CAMPUS MAKERSPACE SYSTEM")
        print("================================")
        print("1. Manage Members")
        print("2. Manage Equipment")
        print("3. Manage Loans")
        print("4. Search")
        print("5. Reports")
        print("0. Exit")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            member_menu()
        elif choice == "2":
            equipment_menu()
        elif choice == "3":
            loan_menu()
        elif choice == "4":
            search_menu()
        elif choice == "5":
            reports_menu()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select a menu option.")


if __name__ == "__main__":
    main()
