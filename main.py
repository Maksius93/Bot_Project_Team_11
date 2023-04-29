from collections import UserDict
import re
from datetime import date
import pickle
import atexit


class AddressBook(UserDict):
    # конструктор AddressBook
    def __init__(self, filename):
        self.filename = filename
        super().__init__()

    # додавання рекорду до AddressBook
    def add_record(self, record):
        self.data[record.name.value] = record

    # видалення рекорду з AddressBook
    def delete_record(self, name):
        del self.data[name]

    def find_records(self, name=None, phone=None):
        search_result = []
        if name:
            if name in address_book.record_list().keys():
                search_result.append(address_book.record_list()[name])
        elif phone:
            for record_key in address_book.record_list().keys():
                if phone in address_book.record_list()[record_key].get_phones():
                    search_result.append(
                        address_book.record_list()[record_key])
        return search_result

    # отримання списку рекордів з AddressBook
    def record_list(self):
        return self.data

    def iterator(self, page_size=10):
        page_start = 0
        page_end = page_size
        while page_start < len(self.record_list()):
            yield list(self.record_list().values())[page_start:page_end]
            page_start += page_size
            page_end += page_size

    def save(self):
        with open(self.filename, 'wb') as file:
            pickle.dump(self.data, file)

    def load(self):
        with open(self.filename, 'rb') as file:
            self.data = pickle.load(file)

    def find_by_query(self, query):
        result = []
        if any(char.isdigit() for char in query):
            for record in self.data.values():
                if any(query_number in phone for phone in record.phones for query_number in query if query_number.isdigit()):
                    result.append(record)
        else:
            for record in self.data.values():
                if query.lower() in record.name.value.lower():
                    result.append(record)
        return result


class Field:
    # конструктор Field
    def __init__(self, value=None):
        self.value = value

    # повертає рядок, що містить значення поля
    def __str__(self):
        return str(self.value)

    # повертає рядок, який можна використати для створення нового екземпляру поля
    def __repr__(self):
        return f"{self.__class__.__name__}('{self.value}')"


class Name(Field):
    # конструктор Name
    def __init__(self, value):
        super().__init__(value=value)
        if not self.value:
            raise ValueError('Name should not be empty')


class Phone(Field):
    # конструктор Phone
    def __init__(self, value=None):
        super().__init__(value=value)

    # метод для відображення телефонного номера у зручному форматі
    def __str__(self):
        if self.value:
            # return f"+{self.value[:1]} ({self.value[1:4]}) {self.value[4:7]}-{self.value[7:]}"
            return str(self.value)
        else:
            return ""


class Birthday(Field):
    # конструктор Birthday
    def __init__(self, value=None):
        super().__init__(value)

    def __str__(self):
        return f"{self.day:02d}.{self.month:02d}.{self.year}"


class Record:
    # конструктор Record
    def __init__(self, name, phone=None, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = birthday

    @property
    def phone(self):
        return self._phone

    @phone.setter
    def phone(self, value):
        if not re.match(r"^\d{10}$", value):
            raise ValueError('Phone number must be a 10-digit number')
        self._phone = value

    @property
    def birthday(self):
        return self._birthday

    @birthday.setter
    def birthday(self, value):
        if value and not re.match(r'^\d{4}-\d{2}-\d{2}$', value):
            raise ValueError("Invalid date format, should be YYYY-MM-DD")
        self._birthday = value

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
        return self.phones

    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone
                break
        return new_phone

    def get_phones(self):
        return [str(phone) for phone in self.phones]

    # метод для обрахування кількості днів до наступного дня народження
    def days_to_birthday(self):
        if not self.value:
            return None
        today = date.today()
        birthday = date(today.year, self.value.month, self.value.day)
        if birthday < today:
            birthday = date(today.year + 1, self.value.month, self.value.day)
        days_to_birthday = (birthday - today).days
        return days_to_birthday

# декоратор


def input_error(func):
    def parsing_error(command):
        try:
            func(command)
        except AttributeError:
            print("Name or phone are not correct")
            return None
        except TypeError:
            print("Something is wrong!")
            return None
        return func(command)
    return parsing_error

# пошук номеру телефону в команді


@input_error
def find_phone(command):
    phone = (re.search(r"[\+]?(38)?(\d|\(|\)|\-){10,17}", command)).group()
    return phone

# приведення номеру телефону до стандартного вигляду


def sanitize_phone_number(phone):
    new_phone = (
        phone.strip()
        .removeprefix("+")
        .replace("(", "")
        .replace(")", "")
        .replace("-", "")
        .replace(" ", "")
    )
    return new_phone

# пошук імені контакта у команді


@input_error
def find_name(command):
    name = (re.search(r"\s[A-Z][a-z]+([\-][A-Z][a-z]+|)?", command)).group()
    return name.strip()

# функція для того, щоб програма не втрачала дані після виходу з програми та відновлювала їх з файлу


def exit_handler():
    address_book.save()


atexit.register(exit_handler)
address_book = AddressBook('address_book.pickle')

# головна функція


def main():
    try:
        address_book.load()
    except FileNotFoundError:
        pass
    while True:
        command = input('>>')
        command_for_check = command.lower()

        # команда для закриття
        if command_for_check in ['good buy', 'close', 'exit']:
            print("Good bye!")
            break

        # команда для привітання
        elif command_for_check in ['hello', 'hi', 'good morning', 'good afternoon', 'good evening']:
            print("How can I help you?")

        # команда для додавання нового контакту
        elif 'add' in command.lower():
            phone = find_phone(command)
            name = find_name(command)
            if phone != None and name != None:
                records_list = address_book.find_records(name, None)
                if len(records_list) == 0:
                    records_list = [Record(name)]
                for record in records_list:
                    if phone in record.get_phones():
                        print('Phone is already added.')
                        break
                    else:
                        record.add_phone(sanitize_phone_number(phone))
                        address_book.add_record(record)
                        print('Contact is added')

        # команда для зміни номеру телефону для існуючого контакту
        elif 'change' in command.lower():
            phone = find_phone(command)
            name = find_name(command)
            record = Record(name)
            if name in address_book.record_list():
                old_phone = address_book.record_list()[name].get_phones()
                new_phone = sanitize_phone_number(phone)
                changed_phone = record.edit_phone(old_phone, new_phone)
                record.add_phone(changed_phone)
                address_book.add_record(record)
                print('Contact is changed')
            else:
                print('Contact with this name was not found.')
                continue

        # команда для видалення контакта
        elif 'remove' in command.lower() or 'delete' in command.lower():
            name = find_name(command)
            phone = find_phone(command)
            records_list = address_book.find_records(name, None)
            if len(records_list) == 0:
                records_list = [Record(name)]
            for record in records_list:
                if name in address_book.record_list():
                    if phone in address_book.record_list()[name].get_phones():
                        changed_phone = record.remove_phone(phone)
                        record.add_phone(changed_phone)
                        address_book.add_record(record)
                        print('Phone is removed')
                    else:
                        print('Phone not found for this name')
                    break
                else:
                    print('Contact not found')

        # команда для виводу номеру телефону для існуючого контакту
        elif 'phone' in command.lower():
            phone = find_phone(command)
            name = find_name(command)
            if phone == None and record.name.value not in address_book.record_list():
                print('Contact with this name was not found')
            elif phone == None and name != None:
                records_list = address_book.find_records(name, None)
                for record in records_list:
                    phone = record.get_phones()
                    print('Phone number of ', name, ': ', phone)
            elif phone == None and name == None:
                name = input(
                    'Name is not entered. Enter the name of contact: \n>>')

        # команда для виводу всіх даних телефонної книги (словника)
        elif 'show all' in command.lower():
            if len(address_book.record_list()) > 0:
                for name in address_book.record_list():
                    record = address_book[name]
                    phones = record.get_phones()
                    if phones == ["[Phone('[...]')]"]:
                        print(name, ": no phone numbers")
                    elif len(phones) > 0:
                        # використовувати ітератор для виведення записів по сторінках
                        for page in address_book.iterator(page_size=5):
                            if record in page:
                                print(name, ":", phones)
                    else:
                        print(name, ": no phone numbers")

            else:
                print("You don't have any contacts in your dict")
        elif 'save data' in command.lower():
            address_book.save()
        # результат, якщо команда не знайдена
        else:
            print('Unknown command. Please, enter another one')


main()
