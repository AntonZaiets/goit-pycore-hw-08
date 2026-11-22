from models import AddressBook, Record
from decorators import input_error

# return the record or raise KeyError if it does not exist
def get_record(book: AddressBook, name: str) -> Record:
    record = book.find(name)
    if record is None:
        raise KeyError(name)
    return record


# add a new contact or a phone to an existing one
@input_error
def add_contact(args, book: AddressBook):
    if len(args) < 2:
        raise ValueError("Usage: add [name] [phone]")
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    record.add_phone(phone)
    return message


# change a phone number for a contact
@input_error
def change_contact(args, book: AddressBook):
    if len(args) < 3:
        raise ValueError("Usage: change [name] [old phone] [new phone]")
    name, old_phone, new_phone, *_ = args
    record = get_record(book, name)
    record.edit_phone(old_phone, new_phone)
    return "Contact updated."


# show all phones of a contact
@input_error
def show_phone(args, book: AddressBook):
    name = args[0]
    record = get_record(book, name)
    if not record.phones:
        return f"{name} has no phones."
    return f"{name}: {'; '.join(p.value for p in record.phones)}"


# show all contacts in the address book
@input_error
def show_all(book: AddressBook):
    if not book.data:
        return "No contacts saved."
    return "\n".join(str(record) for record in book.data.values())


# add a birthday to a contact
@input_error
def add_birthday(args, book: AddressBook):
    if len(args) < 2:
        raise ValueError("Usage: add-birthday [name] [DD.MM.YYYY]")
    name, birthday, *_ = args
    record = get_record(book, name)
    record.add_birthday(birthday)
    return "Birthday added."


# show the birthday of a contact
@input_error
def show_birthday(args, book: AddressBook):
    name = args[0]
    record = get_record(book, name)
    if record.birthday is None:
        return f"{name} has no birthday set."
    return f"{name}: {record.birthday}"


# show birthdays to celebrate during the next week
@input_error
def birthdays(args, book: AddressBook):
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No birthdays in the next week."
    return "\n".join(
        f"{item['name']}: {item['congratulation_date']}" for item in upcoming
    )
