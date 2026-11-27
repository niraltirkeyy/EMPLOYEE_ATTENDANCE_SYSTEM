
import json
import calendar
from datetime import datetime


# CLASS 1: Employee
class Employee:

    def __init__(self, emp_id, name):
        self.emp_id = emp_id
        self.name = name
        self.records = []

    # Mark employee attendance
    def mark_attendance(self, date, status):

        for record in self.records:
            if record["date"] == date:
                return False

        self.records.append({
            "date": date,
            "status": status
        })

        self.records.sort(key=lambda record: record["date"])

        return True


# CLASS 2: Attendance System
class AttendanceSystem:

    def __init__(self):
        self.employees = []
        self.file = "attendance.txt"
        self.load_data()

    # Load saved employee data
    def load_data(self):

        try:
            with open(self.file, "r") as file:
                data = json.load(file)

            for item in data:
                employee = Employee(item["id"], item["name"])
                employee.records = item.get("records", [])
                self.employees.append(employee)

        except (FileNotFoundError, json.JSONDecodeError):
            self.employees = []

    # Save employee data
    def save_data(self):

        data = []

        for employee in self.employees:
            data.append({
                "id": employee.emp_id,
                "name": employee.name,
                "records": employee.records
            })

        with open(self.file, "w") as file:
            json.dump(data, file, indent=4)

    # Generate unique employee ID
    def generate_employee_id(self):

        highest_id = 100

        for employee in self.employees:
            try:
                number = int(employee.emp_id[1:])
                highest_id = max(highest_id, number)
            except (ValueError, IndexError):
                continue

        return f"E{highest_id + 1}"

    # Find employee using ID
    def find_employee(self, emp_id):

        for employee in self.employees:
            if employee.emp_id == emp_id:
                return employee

        return None

    # Add new employee
    def add_employee(self):

        name = input("Enter employee name: ").strip()

        if not name:
            print("Name cannot be empty.")
            return

        emp_id = self.generate_employee_id()

        employee = Employee(emp_id, name)

        self.employees.append(employee)
        self.save_data()

        print(f"\nEmployee added successfully!")
        print(f"Employee ID: {emp_id}")
        print(f"Employee Name: {name}")

    # Display all employees
    def show_employees(self):

        if not self.employees:
            print("\nNo employees registered.")
            return

        print("\n========== EMPLOYEE LIST ==========")
        print(f"{'ID':<12}{'EMPLOYEE NAME':<25}")
        print("-" * 37)

        for employee in self.employees:
            print(f"{employee.emp_id:<12}{employee.name:<25}")

    # Mark attendance
    def mark_attendance(self):

        emp_id = input("Enter employee ID: ").strip().upper()

        employee = self.find_employee(emp_id)

        if employee is None:
            print(f"Employee {emp_id} not found.")
            return

        date = input("Enter date (YYYY-MM-DD): ").strip()

        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            print("Invalid date. Use YYYY-MM-DD.")
            return

        status = input("Enter status (P/A/L): ").upper().strip()

        if status not in ["P", "A", "L"]:
            print("Invalid status. Enter P, A or L.")
            return

        result = employee.mark_attendance(date, status)

        if result:
            self.save_data()
            print("Attendance marked successfully!")
        else:
            print(f"Attendance for {date} is already marked.")

    # Display monthly attendance calendar
    def show_calendar(self):

        emp_id = input("Enter employee ID: ").strip().upper()

        employee = self.find_employee(emp_id)

        if employee is None:
            print(f"Employee {emp_id} not found.")
            return

        try:
            year = int(input("Enter year (YYYY): "))
            month = int(input("Enter month (1-12): "))

            if year < 1 or month not in range(1, 13):
                raise ValueError

        except ValueError:
            print("Invalid month or year.")
            return

        print("\n" + "=" * 65)
        print(f"EMPLOYEE: {employee.name}")
        print(f"EMPLOYEE ID: {employee.emp_id}")
        print(f"ATTENDANCE CALENDAR: {calendar.month_name[month]} {year}")
        print("=" * 65)

        # Store attendance records by date
        attendance = {}

        for record in employee.records:
            record_date = datetime.strptime(
                record["date"], "%Y-%m-%d"
            )

            if record_date.year == year and record_date.month == month:
                attendance[record_date.day] = record["status"]

        # Calendar columns
        print(
            f"{'SUN':<9}{'MON':<9}{'TUE':<9}"
            f"{'WED':<9}{'THU':<9}{'FRI':<9}{'SAT':<9}"
        )

        print("-" * 63)

        # Generate calendar weeks
        month_weeks = calendar.monthcalendar(year, month)

        for week in month_weeks:

            for day in week:

                if day == 0:
                    cell = ""
                else:
                    status = attendance.get(day, "-")
                    cell = f"{day:02d} {status}"

                print(f"{cell:<9}", end="")

            print()

        print("-" * 63)
        print("P = Present | A = Absent | L = Leave | - = Not Marked")

    # Generate attendance report
    def show_report(self):

        emp_id = input("Enter employee ID: ").strip().upper()

        employee = self.find_employee(emp_id)

        if employee is None:
            print(f"Employee {emp_id} not found.")
            return

        present = 0
        absent = 0
        leave = 0

        for record in employee.records:

            if record["status"] == "P":
                present += 1

            elif record["status"] == "A":
                absent += 1

            elif record["status"] == "L":
                leave += 1

        total = len(employee.records)

        percentage = (present / total * 100) if total > 0 else 0

        print("\n========== ATTENDANCE REPORT ==========")
        print(f"Employee ID: {employee.emp_id}")
        print(f"Employee Name: {employee.name}")
        print("-" * 40)
        print(f"Total Recorded Days : {total}")
        print(f"Present Days        : {present}")
        print(f"Absent Days         : {absent}")
        print(f"Leave Days          : {leave}")
        print("-" * 40)

        if total == 0:
            print("Attendance: 0.00% (No records)")
        else:
            print(f"Attendance: {percentage:.2f}%")

    # Main menu
    def menu(self):

        while True:

            print("\n===== EMPLOYEE ATTENDANCE SYSTEM =====")
            print("1. Add Employee")
            print("2. View Employee List")
            print("3. Mark Attendance")
            print("4. View Monthly Attendance Calendar")
            print("5. View Attendance Report")
            print("6. Exit")

            choice = input("\nEnter your choice: ").strip()

            if choice == "1":
                self.add_employee()

            elif choice == "2":
                self.show_employees()

            elif choice == "3":
                self.mark_attendance()

            elif choice == "4":
                self.show_calendar()

            elif choice == "5":
                self.show_report()

            elif choice == "6":
                print("Thank you for using the system!")
                break

            else:
                print("Invalid choice. Try again.")


# MAIN PROGRAM
if __name__ == "__main__":
    system = AttendanceSystem()
    system.menu()
