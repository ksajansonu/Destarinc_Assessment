# Importing the required module for JSON file handling
import json
import os

# Get the current directory of the Python file
current_directory = os.path.dirname(os.path.abspath(__file__))

class Employee:
    def __init__(self, name, emp_id, title, department):
        self.name = name
        self.emp_id = emp_id
        self.title = title
        self.department = department

    def display_details(self):
        print(f"Name: {self.name}")
        print(f"ID: {self.emp_id}")
        print(f"Title: {self.title}")
        print(f"Department: {self.department}")

    def __str__(self):
        return f"{self.name} (ID: {self.emp_id})"


class Department:
    def __init__(self, name):
        self.name = name
        self.employees = []

    def add_employee(self, employee):
        self.employees.append(employee)

    def remove_employee(self, employee):
        if employee in self.employees:
            self.employees.remove(employee)
        else:
            print("Employee not found in this department.")

    def list_employees(self):
        print(f"Employees in {self.name} department:")
        for emp in self.employees:
            print(emp)

    def __str__(self):
        return f"Department: {self.name}"


class Company:
    def __init__(self):
        self.departments = {}

    def add_department(self, department):
        if department.name not in self.departments:
            self.departments[department.name] = department
        else:
            print("Department already exists.")

    def remove_department(self, department_name):
        if department_name in self.departments:
            del self.departments[department_name]
        else:
            print("Department not found.")

    def display_departments(self):
        print("Departments in the company:")
        for department in self.departments.values():
            print(department)

    def save_to_file(self, filename):
        with open(filename, 'w') as f:
            data = {department.name: [emp.name for emp in department.employees] for department in self.departments.values()}
            json.dump(data, f, indent=4)

    def load_from_file(self, filename):
        with open(filename, 'r') as f:
            data = json.load(f)
            for department_name, employee_names in data.items():
                department = Department(department_name)
                self.add_department(department)
                for emp_name in employee_names:
                    emp_id = len(department.employees) + 1
                    employee = Employee(emp_name, emp_id, "Employee", department_name)
                    department.add_employee(employee)


def print_menu():
    print("\nEmployee Management System Menu:")
    print("1. Add Employee")
    print("2. Remove Employee")
    print("3. Display Department")
    print("4. Add Department")
    print("5. Remove Department")
    print("6. Display All Departments")
    print("7. Save Company Data to File")
    print("8. Load Company Data from File")
    print("9. Exit")


if __name__ == "__main__":
    company = Company()
    filename = f"{current_directory}/company_data.json"

    while True:
        print_menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            pass  # Add Employee functionality
        elif choice == "2":
            pass  # Remove Employee functionality
        elif choice == "3":
            pass  # Display Department functionality
        elif choice == "4":
            pass  # Add Department functionality
        elif choice == "5":
            pass  # Remove Department functionality
        elif choice == "6":
            pass  # Display All Departments functionality
        elif choice == "7":
            pass  # Save Company Data to File functionality
        elif choice == "8":
            pass  # Load Company Data from File functionality
        elif choice == "9":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 9.")
