from datetime import date, datetime

from database import execute_query, fetch_all, fetch_one
from models import Member, Equipment, Loan


def validate_text(value, field_name):
    if not value.strip():
        raise ValueError(f"{field_name} cannot be empty.")


def validate_date(date_text):
    try:
        datetime.strptime(date_text, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Date must use YYYY-MM-DD format.")


# -------------------------
# MEMBER OPERATIONS
# -------------------------

def register_member(name, email, phone):
    validate_text(name, "Name")
    validate_text(email, "Email")
    validate_text(phone, "Phone")

    existing = fetch_one(
        "SELECT member_id FROM members WHERE email = ?",
        (email,),
    )

    if existing:
        raise ValueError("A member with that email already exists.")

    member_id, _ = execute_query(
        """
        INSERT INTO members (name, email, phone)
        VALUES (?, ?, ?)
        """,
        (name, email, phone),
    )

    return member_id


def list_members():
    rows = fetch_all("""
        SELECT member_id, name, email, phone, status
        FROM members
        ORDER BY member_id
    """)

    if not rows:
        print("No members found.")
        return

    print("\n--- MEMBER LIST ---")
    for row in rows:
        member = Member(*row)
        print(member.display_info())


def update_member(member_id, name, email, phone):
    validate_text(name, "Name")
    validate_text(email, "Email")
    validate_text(phone, "Phone")

    existing = fetch_one(
        "SELECT member_id FROM members WHERE member_id = ?",
        (member_id,),
    )

    if not existing:
        return False

    duplicate = fetch_one(
        """
        SELECT member_id
        FROM members
        WHERE email = ? AND member_id != ?
        """,
        (email, member_id),
    )

    if duplicate:
        raise ValueError("Another member already uses that email.")

    execute_query(
        """
        UPDATE members
        SET name = ?, email = ?, phone = ?
        WHERE member_id = ?
        """,
        (name, email, phone, member_id),
    )

    return True


# -------------------------
# EQUIPMENT OPERATIONS
# -------------------------

def register_equipment(name, category):
    validate_text(name, "Equipment name")
    validate_text(category, "Category")

    equipment_id, _ = execute_query(
        """
        INSERT INTO equipment (name, category, status)
        VALUES (?, ?, 'available')
        """,
        (name, category),
    )

    return equipment_id


def list_equipment():
    rows = fetch_all("""
        SELECT equipment_id, name, category, status
        FROM equipment
        ORDER BY equipment_id
    """)

    if not rows:
        print("No equipment found.")
        return

    print("\n--- EQUIPMENT LIST ---")
    for row in rows:
        equipment = Equipment(*row)
        print(equipment.display_info())


def update_equipment(equipment_id, name, category, status):
    validate_text(name, "Equipment name")
    validate_text(category, "Category")

    if status not in ("available", "maintenance"):
        raise ValueError("Invalid equipment status.")

    equipment_row = fetch_one(
        """
        SELECT equipment_id, name, category, status
        FROM equipment
        WHERE equipment_id = ?
        """,
        (equipment_id,),
    )

    if not equipment_row:
        return False

    equipment = Equipment(*equipment_row)

    # Borrowed equipment should only become available through returning its loan.
    if equipment.status == "borrowed" and status == "available":
        raise ValueError(
            "Borrowed equipment must be returned through the loan menu."
        )

    execute_query(
        """
        UPDATE equipment
        SET name = ?, category = ?, status = ?
        WHERE equipment_id = ?
        """,
        (name, category, status, equipment_id),
    )

    return True


# -------------------------
# LOAN OPERATIONS
# -------------------------

def create_loan(member_id, equipment_id, due_date):
    validate_date(due_date)

    if due_date < date.today().isoformat():
        raise ValueError("Due date cannot be before today.")

    member_row = fetch_one(
        """
        SELECT member_id, name, email, phone, status
        FROM members
        WHERE member_id = ?
        """,
        (member_id,),
    )

    if not member_row:
        raise ValueError("Member does not exist.")

    member = Member(*member_row)

    if member.status != "active":
        raise ValueError("This member is inactive.")

    equipment_row = fetch_one(
        """
        SELECT equipment_id, name, category, status
        FROM equipment
        WHERE equipment_id = ?
        """,
        (equipment_id,),
    )

    if not equipment_row:
        raise ValueError("Equipment does not exist.")

    equipment = Equipment(*equipment_row)

    if not equipment.is_available():
        raise ValueError(
            f"Equipment is not available. Current status: {equipment.status}."
        )

    checkout_date = date.today().isoformat()

    loan_id, _ = execute_query(
        """
        INSERT INTO loans (
            member_id,
            equipment_id,
            checkout_date,
            due_date,
            status
        )
        VALUES (?, ?, ?, ?, 'active')
        """,
        (member_id, equipment_id, checkout_date, due_date),
    )

    execute_query(
        """
        UPDATE equipment
        SET status = 'borrowed'
        WHERE equipment_id = ?
        """,
        (equipment_id,),
    )

    return loan_id


def return_loan(loan_id):
    loan_row = fetch_one(
        """
        SELECT
            loan_id,
            member_id,
            equipment_id,
            checkout_date,
            due_date,
            return_date,
            status
        FROM loans
        WHERE loan_id = ?
        """,
        (loan_id,),
    )

    if not loan_row:
        return False

    loan = Loan(*loan_row)

    if not loan.is_active():
        raise ValueError("This loan has already been returned.")

    loan.close_loan(date.today().isoformat())

    execute_query(
        """
        UPDATE loans
        SET return_date = ?, status = 'returned'
        WHERE loan_id = ?
        """,
        (loan.return_date, loan.loan_id),
    )

    execute_query(
        """
        UPDATE equipment
        SET status = 'available'
        WHERE equipment_id = ?
        """,
        (loan.equipment_id,),
    )

    return True


def list_active_loans():
    rows = fetch_all("""
        SELECT
            loans.loan_id,
            members.name,
            equipment.name,
            loans.checkout_date,
            loans.due_date,
            loans.status
        FROM loans
        JOIN members
            ON loans.member_id = members.member_id
        JOIN equipment
            ON loans.equipment_id = equipment.equipment_id
        WHERE loans.status = 'active'
        ORDER BY loans.loan_id
    """)

    if not rows:
        print("No active loans.")
        return

    print("\n--- ACTIVE LOANS ---")
    for row in rows:
        print(
            f"Loan ID: {row[0]} | "
            f"Member: {row[1]} | "
            f"Equipment: {row[2]} | "
            f"Checked out: {row[3]} | "
            f"Due: {row[4]} | "
            f"Status: {row[5]}"
        )


# -------------------------
# SEARCH
# -------------------------

def search_members(term):
    if not term.strip():
        print("Search term cannot be empty.")
        return

    rows = fetch_all(
        """
        SELECT member_id, name, email, phone, status
        FROM members
        WHERE CAST(member_id AS TEXT) = ?
           OR name LIKE ?
        ORDER BY member_id
        """,
        (term, f"%{term}%"),
    )

    if not rows:
        print("No members found.")
        return

    print("\n--- MEMBER SEARCH RESULTS ---")
    for row in rows:
        member = Member(*row)
        print(member.display_info())


def search_equipment(term):
    if not term.strip():
        print("Search term cannot be empty.")
        return

    rows = fetch_all(
        """
        SELECT equipment_id, name, category, status
        FROM equipment
        WHERE CAST(equipment_id AS TEXT) = ?
           OR name LIKE ?
        ORDER BY equipment_id
        """,
        (term, f"%{term}%"),
    )

    if not rows:
        print("No equipment found.")
        return

    print("\n--- EQUIPMENT SEARCH RESULTS ---")
    for row in rows:
        equipment = Equipment(*row)
        print(equipment.display_info())


# -------------------------
# REPORTS
# -------------------------

def report_overdue_loans():
    today = date.today().isoformat()

    rows = fetch_all(
        """
        SELECT
            loans.loan_id,
            members.name,
            equipment.name,
            loans.checkout_date,
            loans.due_date
        FROM loans
        JOIN members
            ON loans.member_id = members.member_id
        JOIN equipment
            ON loans.equipment_id = equipment.equipment_id
        WHERE loans.status = 'active'
          AND loans.due_date < ?
        ORDER BY loans.due_date
        """,
        (today,),
    )

    if not rows:
        print("No overdue loans.")
        return

    print("\n--- OVERDUE LOANS ---")
    for row in rows:
        print(
            f"Loan ID: {row[0]} | "
            f"Member: {row[1]} | "
            f"Equipment: {row[2]} | "
            f"Checked out: {row[3]} | "
            f"Due: {row[4]}"
        )


def report_equipment_by_category():
    rows = fetch_all("""
        SELECT
            category,
            COUNT(*) AS equipment_count
        FROM equipment
        GROUP BY category
        ORDER BY category
    """)

    if not rows:
        print("No equipment found.")
        return

    print("\n--- EQUIPMENT BY CATEGORY ---")
    for category, count in rows:
        print(f"{category}: {count}")


def report_member_loan_history(member_id):
    member = fetch_one(
        "SELECT member_id, name FROM members WHERE member_id = ?",
        (member_id,),
    )

    if not member:
        print("Member not found.")
        return

    rows = fetch_all(
        """
        SELECT
            loans.loan_id,
            equipment.name,
            loans.checkout_date,
            loans.due_date,
            loans.return_date,
            loans.status
        FROM loans
        JOIN equipment
            ON loans.equipment_id = equipment.equipment_id
        WHERE loans.member_id = ?
        ORDER BY loans.loan_id
        """,
        (member_id,),
    )

    print(f"\n--- LOAN HISTORY: {member[1]} ---")

    if not rows:
        print("This member has no loan history.")
        return

    for row in rows:
        print(
            f"Loan ID: {row[0]} | "
            f"Equipment: {row[1]} | "
            f"Checked out: {row[2]} | "
            f"Due: {row[3]} | "
            f"Returned: {row[4] or 'Not returned'} | "
            f"Status: {row[5]}"
        )
