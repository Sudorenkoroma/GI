from collections import UserDict
import re
from datetime import datetime
from datetime import timedelta
import pickle


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if not self.validate(value):
            raise ValueError("Phone number must be 10 digits")
        super().__init__(value)

    def validate(self, value):
        return re.fullmatch(r'\d{10}', value) is not None


class Birthday(Field):
    def __init__(self, value):
        try:
            value = datetime.strptime(value, '%d.%m.%Y').date()
            super().__init__(value)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, add_phone):
        self.phones.append(Phone(add_phone))


    def edit_phone(self, old, new):
        if any(phone.value == new for phone in self.phones):
            return f"New phone number {new} already exists."
        for phone in self.phones:
            if phone.value == old:
                phone.value = new
                return "Phone updated."
        return "Old phone not found."

    def add_birthday(self, value):
        self.birthday = Birthday(value)

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record):
        if record.name.value in self.data:
            existing_record = self.data[record.name.value]
            added_phones = False  # Flag to track if any new phone was actually added
            for new_phone in record.phones:
                if not any(existing_phone.value == new_phone.value for existing_phone in existing_record.phones):
                    existing_record.phones.append(new_phone)
                    added_phones = True
            if added_phones:
                return "New phone(s) added to existing contact."
            else:
                return "No new phone added; phone already exists."
        else:
            self.data[record.name.value] = record
            return "New contact created."

    def get_upcoming_birthdays(self):
        today = datetime.today().date()
        upcoming_birthdays = ""

        for user in self.data:
            birthday = self.data[user].birthday.value
            birthday_this_year = birthday.replace(year=today.year)
            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(year=today.year + 1)

            days_until_birthday = (birthday_this_year - today).days

            if days_until_birthday <= 7:
                if birthday_this_year.weekday() >= 5:
                    days_add_if_holiday = (7 - birthday_this_year.weekday())
                    birthday_this_year += timedelta(days_add_if_holiday)
                congratulation_date = birthday_this_year.strftime("%Y.%m.%d")
                upcoming_birthdays += "\n"+f"{self.data[user].name.value} has congratulation date {congratulation_date}"

        return upcoming_birthdays


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as error:
            return error
        except IndexError:
            return "Enter the argument for the command."
        except KeyError:
            return "Contact not found."

    return inner


@input_error
def parse_input(user_input):
    parts = user_input.strip().split(' ', 3)
    command = parts[0].lower()
    args = parts[1:] if len(parts) > 1 else []
    return command, args


@input_error
def add_contact(args, book):
    if len(args) != 2:
        return r"Invalid input. Usage: add [name] [phone]"
    name, phone = args
    record = Record(name)
    record.add_phone(phone)
    result_2 = book.add_record(record)
    return f"{result_2}"


@input_error
def change_contact(args, book):
    if len(args) != 3:
        return f"Invalid input. Usage: change [name] [old_phone] [new_phone]"
    name, old_phone, new_phone = args
    result = book[name].edit_phone(old_phone, new_phone)
    return result


@input_error
def show_phone(args, book):
    if len(args) != 1:
        return f"Invalid input. Usage: phone [name]"
    name = args[0]
    if name in book:
        return book[name]
    else:
        return f"Contact not found."


@input_error
def show_all(book):
    return "\n".join(str(record) for record in book.values())


@input_error
def add_birthday(args, book):
    if len(args) != 2:
        return f"Invalid input. Usage: add-bd [name] [birthday]"
    name, date = args
    if name in book:
        book[name].add_birthday(date)
        return f"Birthday added for {name}."
    else:
        return f"Contact not found."

@input_error
def show_birthday(args, book):
    name = args[0]
    birthday = (book[name].birthday.value)
    return f"{name} was born {birthday}"

@input_error
def birthdays(book):
    result = book.get_upcoming_birthdays()
    return result

def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()  # Повернення нової адресної книги, якщо файл не знайдено

def main():
    book = load_data()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            save_data(book)
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(show_all(book))
        elif command == "add-bd":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(book))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()