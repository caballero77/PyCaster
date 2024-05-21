import re
import pickle
from pathlib import Path
from typing import Tuple
from datetime import datetime
from collections import UserDict

class Field:
    """Base class for fields of the record"""
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    """Class for name field of the record"""
    pass

class Phone(Field):
    """Class for phone field of the record"""
    def __init__(self, value):
        if not self.validate(value):
            raise ValueError('Invalid phone number')
        
        super().__init__(value)

    @staticmethod
    def validate(value: str) -> bool:
        """Validate phone number
        
        Args:
            value: str: phone number
        
        Returns:
            bool: True if phone number is valid, False otherwise"""
        return bool(re.match(r"^(\+38)?(0\d{9})$", value))
    
class Birthday(Field):
    def __init__(self, value):
        if not self.validate(value):
            raise ValueError('Invalid date format. Use DD.MM.YYYY')
        
        super().__init__(datetime.strptime(value, "%d.%m.%Y").date())
    
    @staticmethod
    def validate(value: str) -> bool:
        try:
            datetime.strptime(value, "%d.%m.%Y")
            return True
        except ValueError:
            return False

class Record:
    """Class for record, which contains name and phones of the contact"""
    def __init__(self, name):
        self.name: str = Name(name)
        self.phones: list[str] = []
        self.birthday: Birthday = None

    def add_phone(self, phone: str) -> bool:
        """Add phone to the record
        
        Args:
            phone: str: phone number
        
        Returns:
            bool: True if phone was added, False if phone already exists"""
        if self.find_phone(phone):
            return False
        self.phones.append(Phone(phone))
        return True
    
    def add_birthday(self, birthday: str) -> bool:
        try:
            self.birthday = Birthday(birthday)
        except ValueError:
            return False
        return True
    
    def delete_phone(self, phone_number: str) -> bool:
        """Delete phone from the record
        
        Args:
            phone_number: str: phone number
            
        Returns:
            bool: True if phone was deleted, False if phone not found"""
        phone = self.find_phone(phone_number)
        if phone:
            self.phones.remove(phone)
            return True
        return False
    
    def edit_phone(self, phone_number: str, new_phone: str) -> bool:
        """Edit phone in the record
        
        Args:
            phone_number: str: phone number
            new_phone: str: new phone number
        
        Returns:
            bool: True if phone was edited, False if phone not found"""
        phone = self.find_phone(phone_number)
        if phone:
            phone.value = new_phone
            return True
        return False

    def find_phone(self, phone_number: str) -> Phone:
        """Find phone in the record
        
        Args:
            phone_number: str: phone number
            
        Returns:
            Phone: phone object if phone was found, None if phone not found"""
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None
    
    def __str__(self):
        return f"Contact name: {self.name.value} " + \
            (f"birthday: {self.birthday.value}, " if self.birthday else "") + \
            (f"phones: {'; '.join(p.value for p in self.phones)}" if self.phones else "")

class AddressBook(UserDict):
    """Class for address book, which contains records of contacts"""
    def __init__(self):
        super().__init__()

    def add_record(self, record: Record) -> bool:
        """Add record to the address book
        
        Args:
            record: Record: record object
        
        Returns:
            bool: True if record was added, False if record already exists"""
        if self.has_record(record.name.value):
            return False

        self.data[record.name.value] = record
        return True
    
    def delete(self, name: str) -> bool:
        """Delete record from the address book
        
        Args:
            name: str: name of the contact
            
        Returns:
            bool: True if record was deleted, False if record not found"""
        if self.has_record(name):
            del self.data[name]
            return True
        return False
    
    def find(self, name: str) -> Record:
        """Find record in the address book
        
        Args:
            name: str: name of the contact
            
        Returns:
            Record: record object if record was found, None if record not found"""
        return self.data.get(name)
    
    def has_record(self, name: str) -> bool:
        """Check if record exists in the address book
        
        Args:
            name: str: name of the contact
        
        Returns:
            bool: True if record exists, False if record not found"""
        return self.data.get(name) is not None
    
    @staticmethod
    def get_next_birthday(today, birth_date):
        """Get next birthday date for user. If birthday is already passed this year, return next year's date.
        
        Args:
            today (datetime): current date
            birth_date (datetime): user's birth date
        """
        birth_date = birth_date.replace(year=today.year)
        if birth_date < today:
            birth_date = birth_date.replace(year=today.year + 1)
        return birth_date

    @staticmethod
    def get_next_weekday(date):
        """If birthday is on weekend, move it to the nearest weekday of next week."""
        if date.weekday() == 5: # Saturday
            date = date.replace(day=date.day + 2)
        elif date.weekday() == 6: # Sunday
            date = date.replace(day=date.day + 1)
        return date

    def get_upcoming_birthdays(self):
        """Get upcoming birthdays for the next week from the address book"""
        today = datetime.today().date()
        upcoming_birthdays = []
        for record in self.data.values():
            if record.birthday is None:
                continue
            next_birthday = self.get_next_birthday(today, record.birthday.value)
            if (next_birthday - today).days <= 7:
                upcoming_birthdays.append({'name': record.name, 'congratulation_date': self.get_next_weekday(next_birthday).strftime("%Y.%m.%d")})
        return upcoming_birthdays
    
    @staticmethod
    def load_data(file_path: Path) -> Tuple['AddressBook', str]:
        """Load data from file
        
        Args:
            file_path: str: file path
            
        Returns:
            Tuple[AddressBook, str]: address book object and error message if any"""
        try:
            if not file_path.parent.exists():
                return None, f"Can't find the directory: {file_path.parent}"
            if not file_path.exists():
                return AddressBook(), None
            with open(file_path, 'rb') as file:
                return pickle.load(file), None
        except Exception as e:
            return None, str(e)
        
    def save_data(self, file_path: Path) -> str:
        """Save data to file
        
        Args:
            file_path: str: file path
            
        Returns:
            str: error message if any"""
        try:
            if not file_path.exists():
                file_path.touch()
            with open(file_path, 'wb') as file:
                pickle.dump(self, file)
            return None
        except Exception as e:
            return str(e)