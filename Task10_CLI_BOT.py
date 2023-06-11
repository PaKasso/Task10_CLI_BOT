from collections import UserDict


class AddressBook(UserDict):
    def find_records(self, criteria):
        result = []
        for record in self.values():
            if record.matches(criteria):
                result.append(record)
        return result


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.fields = []

    def add_field(self, field):
        self.fields.append(field)

    def remove_field(self, field):
        self.fields.remove(field)

    def edit_field(self, old_field, new_field):
        index = self.fields.index(old_field)
        self.fields[index] = new_field

    def matches(self, criteria):
        for field in self.fields:
            if field.matches(criteria):
                return True
        return False


class Field:
    def __init__(self, value):
        self.value = value

    def matches(self, criteria):
        return False


class Name(Field):
    def matches(self, criteria):
        return self.value.lower() == criteria.lower()


class Phone(Field):
    def matches(self, criteria):
        return self.value.lower() == criteria.lower()


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Invalid command. Please try again."
        except ValueError:
            return "Invalid input. Please try again."
        except IndexError:
            return "Invalid command. Please try again."
    return wrapper


address_book = AddressBook()


@input_error
def add_contact(name, phone):
    record = Record(name)
    phone_field = Phone(phone)
    record.add_field(phone_field)
    address_book.add_record(record)
    return "Contact added successfully."


@input_error
def change_phone(name, phone):
    records = address_book.find_records(name)
    if len(records) == 0:
        return "Contact not found."
    for record in records:
        for field in record.fields:
            if isinstance(field, Phone):
                field.value = phone
    return "Phone number updated successfully."


@input_error
def get_phone(name):
    records = address_book.find_records(name)
    if len(records) == 0:
        return "Contact not found."
    result = ""
    for record in records:
        for field in record.fields:
            if isinstance(field, Phone):
                result += f"{record.name.value}: {field.value}\n"
    return result.strip()


@input_error
def show_all_contacts():
    records = address_book.values()
    if not records:
        return "No contacts found."
    result = "Contacts:\n"
    for record in records:
        result += f"{record.name.value}: "
        for field in record.fields:
            if isinstance(field, Phone):
                result += f"{field.value}, "
        result = result.rstrip(", ")
        result += "\n"
    return result.strip()


def main():
    print("Welcome to the Assistant Bot!")
    while True:
        command = input("Enter a command: ").lower()

        if command == "hello":
            print("How can I help you?")
        elif command.startswith("add "):
            _, name, phone = command.split(" ")
            print(add_contact(name, phone))
        elif command.startswith("change "):
            _, name, phone = command.split(" ")
            print(change_phone(name, phone))
        elif command.startswith("phone "):
            _, name = command.split(" ")
            print(get_phone(name))
        elif command == "show all":
            print(show_all_contacts())
        elif command in ["good bye", "close", "exit"]:
            print("Good bye!")
            break
        else:
            print("Invalid command. Please try again.")


if __name__ == "__main__":
    main()
