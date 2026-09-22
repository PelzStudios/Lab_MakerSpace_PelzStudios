class Member:
    """Represents a registered makerspace member."""

    def __init__(self, member_id, name, email, phone, status="active"):
        self.member_id = member_id
        self.name = name
        self.email = email
        self.phone = phone
        self.status = status

    def display_info(self):
        return (
            f"ID: {self.member_id} | "
            f"Name: {self.name} | "
            f"Email: {self.email} | "
            f"Phone: {self.phone} | "
            f"Status: {self.status}"
        )


class Equipment:
    """Represents equipment owned by the makerspace."""

    def __init__(self, equipment_id, name, category, status="available"):
        self.equipment_id = equipment_id
        self.name = name
        self.category = category
        self.status = status

    def is_available(self):
        return self.status == "available"

    def checkout(self):
        if not self.is_available():
            return False
        self.status = "borrowed"
        return True

    def return_item(self):
        self.status = "available"

    def display_info(self):
        return (
            f"ID: {self.equipment_id} | "
            f"Name: {self.name} | "
            f"Category: {self.category} | "
            f"Status: {self.status}"
        )


class Loan:
    """Represents a checkout of equipment by a member."""

    def __init__(
        self,
        loan_id,
        member_id,
        equipment_id,
        checkout_date,
        due_date,
        return_date=None,
        status="active",
    ):
        self.loan_id = loan_id
        self.member_id = member_id
        self.equipment_id = equipment_id
        self.checkout_date = checkout_date
        self.due_date = due_date
        self.return_date = return_date
        self.status = status

    def is_active(self):
        return self.status == "active"

    def close_loan(self, return_date):
        self.return_date = return_date
        self.status = "returned"

    def is_overdue(self, today):
        return self.is_active() and self.due_date < today
