import pickle

from models import AddressBook

DEFAULT_FILENAME = "addressbook.pkl"


# save the address book to a file using pickle
def save_data(book, filename=DEFAULT_FILENAME):
    with open(filename, "wb") as f:
        pickle.dump(book, f)


# load the address book from a file, or return a new one if there is none
def load_data(filename=DEFAULT_FILENAME):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()
    except (EOFError, pickle.UnpicklingError):
        print("Saved data is corrupted, starting with an empty address book.")
        return AddressBook()
