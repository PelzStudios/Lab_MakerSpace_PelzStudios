# Campus MakerSpace Checkout System

A small Object-Oriented Python CLI application backed by SQLite.

## Features

- Register members
- List members
- Update members
- Register equipment
- List equipment
- Update equipment
- Checkout equipment
- Return equipment
- Search members
- Search equipment
- View active loans
- View overdue loans
- View equipment by category
- View a member's loan history
- Input validation
- Persistent SQLite database

## Project Structure

```text
Lab_MakerSpace_YourUsername/
│
├── main.py
├── models.py
├── database.py
├── services.py
├── README.md
├── requirements.txt
└── makerspace.db
```

`makerspace.db` is created automatically the first time the application runs.

## Requirements

- Python 3.10 or newer
- SQLite3 (included with Python)

No external Python packages are required.

## How to Run

Open a terminal in the project folder and run:

```bash
python main.py
```

The application will automatically create the SQLite database and its tables.

## OOP Design

The application uses three main domain classes:

### Member

Represents a person registered with the makerspace.

Attributes:
- member_id
- name
- email
- phone
- status

### Equipment

Represents equipment available in the makerspace.

Attributes:
- equipment_id
- name
- category
- status

Methods include:
- `is_available()`
- `checkout()`
- `return_item()`

### Loan

Represents a checkout between a member and a piece of equipment.

Attributes:
- loan_id
- member_id
- equipment_id
- checkout_date
- due_date
- return_date
- status

Methods include:
- `is_active()`
- `close_loan()`
- `is_overdue()`

## Database Design

The database contains three tables:

### members

Stores registered makerspace members.

### equipment

Stores equipment inventory and its current status.

### loans

Connects members to equipment using foreign keys.

```text
members
   │
   │ member_id
   ▼
 loans
   ▲
   │ equipment_id
   │
equipment
```

This avoids storing the same member and equipment information repeatedly in the loans table.

## Validation

The application checks that:

- Required text fields are not empty
- Member IDs exist before creating loans
- Equipment IDs exist before creating loans
- Members are active before borrowing equipment
- Equipment is available before borrowing
- Due dates use `YYYY-MM-DD`
- Due dates are not in the past
- Already-returned loans cannot be returned again
- Borrowed equipment cannot be manually marked available

## SQL Reports

The application includes multiple reports using SQL queries and joins:

1. Currently borrowed equipment
2. Overdue loans
3. Equipment grouped by category
4. Member loan history

## Sample Data

On the first run, the application creates a few sample members and equipment records so that the system can be demonstrated immediately.

After that, the application uses the existing database and does not recreate the sample records.

## Live Demonstration Suggested Flow

1. Start the application.
2. Show the member list.
3. Show the equipment list.
4. Register a new member.
5. Register a new equipment item.
6. Checkout equipment.
7. Show active loans.
8. Try checking out the same equipment again and show the validation error.
9. Return the equipment.
10. Show that its status changed back to available.
11. Search for a member or equipment item.
12. Demonstrate the reports.
13. Briefly explain the three classes and the three database tables.
