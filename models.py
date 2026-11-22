from collections import UserDict
from datetime import datetime, date, timedelta

# base class for record fields
class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

# contact name. Required field
class Name(Field):
    pass

# phone number with validation (exactly 10 digits)
class Phone(Field):
    def __init__(self, value):
        if not (isinstance(value, str) and value.isdigit() and len(value) == 10):
            raise ValueError("Phone number must contain exactly 10 digits.")
        super().__init__(value)

# birthday stored as a date object, entered as DD.MM.YYYY
class Birthday(Field):
    def __init__(self, value):
        try:
            birthday = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        super().__init__(birthday)

    def __str__(self):
        return self.value.strftime("%d.%m.%Y")

# contact record with a name, phones and an optional birthday
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    # add a new phone to the record
    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    # remove a phone from the record
    def remove_phone(self, phone):
        found = self.find_phone(phone)
        if found is None:
            raise ValueError(f"Phone {phone} not found.")
        self.phones.remove(found)

    # replace an existing phone with a new one
    def edit_phone(self, old_phone, new_phone):
        found = self.find_phone(old_phone)
        if found is None:
            raise ValueError(f"Phone {old_phone} not found.")
        # validate the new number before changing anything
        new = Phone(new_phone)
        self.phones[self.phones.index(found)] = new

    # return the Phone object with the given number, or None
    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    # set the birthday (only one per contact)
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        phones = "; ".join(p.value for p in self.phones) or "no phones"
        result = f"Contact name: {self.name.value}, phones: {phones}"
        if self.birthday:
            result += f", birthday: {self.birthday}"
        return result

# address book that stores records by contact name
class AddressBook(UserDict):
    # add a record to the address book
    def add_record(self, record):
        self.data[record.name.value] = record

    # return the record with the given name, or None
    def find(self, name):
        return self.data.get(name)

    # delete the record with the given name, if it exists
    def delete(self, name):
        self.data.pop(name, None)

    @staticmethod

    # return the birthday in the given year (Feb 29 -> Mar 1)
    def _date_in_year(birthday, year):
        try:
            return birthday.replace(year=year)
        except ValueError:
            return date(year, 3, 1)

    def get_upcoming_birthdays(self, days=7):
        # return contacts to congratulate within the next `days` days
        today = date.today()
        upcoming = []

        for record in self.data.values():
            if record.birthday is None:
                continue

            bday = record.birthday.value
            next_bday = self._date_in_year(bday, today.year)
            # birthday already passed this year -> take next year
            if next_bday < today:
                next_bday = self._date_in_year(bday, today.year + 1)

            if (next_bday - today).days < days:
                # move weekend birthdays to Monday
                if next_bday.weekday() == 5:
                    next_bday += timedelta(days=2)
                elif next_bday.weekday() == 6:
                    next_bday += timedelta(days=1)

                upcoming.append({
                    "name": record.name.value,
                    "congratulation_date": next_bday.strftime("%d.%m.%Y"),
                })

        return upcoming
