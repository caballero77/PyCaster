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

class Address(Field):
    """Class for address field of the record"""
    pass

class Email(Field):
    """Class for email field of the record"""
    def __init__(self, value):
        if not self.validate(value):
            raise ValueError('Invalid email')
        
        super().__init__(value)

    @staticmethod
    def validate(value: str) -> bool:
        """Validate email
        
        Args:
            value: str: email
        
        Returns:
            bool: True if email is valid, False otherwise"""
        return bool(re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", value))

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
    """Class for birthday field of the record"""
    def __init__(self, value):
        if not self.validate(value):
            raise ValueError('Invalid date format. Use DD.MM.YYYY')
        
        super().__init__(datetime.strptime(value, "%d.%m.%Y").date())
    
    @staticmethod
    def validate(value: str) -> bool:
        """Validate birthday
        
        Args:
            value: str: birthday in format DD.MM.YYYY
        
        Returns:
            bool: True if birthday is valid, False otherwise"""
        try:
            datetime.strptime(value, "%d.%m.%Y")
            return True
        except ValueError:
            return False

class Record:
    """Class for record, which contains name and phones of the contact"""
    def __init__(self, name):
        self.name: str = Name(name)
        self.phones: list[Phone] = []
        self.birthday: Birthday = None
        self.email: Email = None
        self.address: Address = None

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
        """Add birthday to the record
        
        Args:
            birthday: str: birthday in format DD.MM.YYYY
            
        Returns:
            bool: True if birthday was added, False if birthday is invalid"""
        try:
            self.birthday = Birthday(birthday)
        except ValueError:
            return False
        return True
    
    def add_address(self, address: str):
        """Add address to the record

        Args:
            address: str: address"""
        self.address = Address(address)
    
    def add_email(self, email: str) -> bool:
        """Add email to the record
        
        Args:
            email: str: email
            
        Returns:
            bool: True if email was added, False if email is invalid"""
        try:
            self.email = Email(email)
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
    
    def edit_birthday(self, new_birthday: str) -> bool:
        """Edit birthday in the record
        
        Args:
            new_birthday: str: new birthday in format DD.MM.YYYY
        
        Returns:
            bool: True if birthday was edited, False if invalid format"""
        try:
            self.birthday = Birthday(new_birthday)
        except ValueError:
            return False
        return True

    def delete_birthday(self) -> bool:
        """Delete birthday from the record"""
        if self.birthday:
            self.birthday = None
            return True
        return False
    
    def edit_address(self, new_address: str) -> bool:
        """Edit address in the record
        
        Args:
            new_address: str: new address
        
        Returns:
            bool: True if address was edited"""
        self.address = Address(new_address)
        return True

    def delete_address(self) -> bool:
        """Delete address from the record"""
        if self.address:
            self.address = None
            return True
        return False

    def edit_email(self, new_email: str) -> bool:
        """Edit email in the record
        
        Args:
            new_email: str: new email
        
        Returns:
            bool: True if email was edited, False if invalid format"""
        try:
            self.email = Email(new_email)
        except ValueError:
            return False
        return True

    def delete_email(self) -> bool:
        """Delete email from the record"""
        if self.email:
            self.email = None
            return True
        return False
    
    def __str__(self):
        return f"Contact name: {self.name.value} " + \
            (f"birthday: {self.birthday.value}, " if self.birthday else "") + \
            (f"phones: {'; '.join(p.value for p in self.phones)} " if self.phones else "") + \
            (f"email: {self.email.value} " if self.email else "") + \
            (f"address: {self.address.value} " if self.address else "")

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
    
    def is_email_unique(self, email: str) -> bool: 
        """Check if email is unique in the address book
        
        Args:
            email: str: email
            
        Returns:
            bool: True if email is unique, False if email already exists in the address book"""
        for record in self.data.values(): 
            if record.email and record.email.value == email: 
                return False 
        return True 
    
    def is_phone_unique(self, phone: str) -> bool:
        """Check if phone is unique in the address book
        
        Args:
            phone: str: phone number
            
        Returns:
            bool: True if phone is unique, False if phone already exists in the address book"""
        for record in self.data.values():
            if record.find_phone(phone):
                return False
        return True
    
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

    def get_upcoming_birthdays(self, birthday_days:int=None):
        """Get upcoming birthdays for the next week from the address book"""
        today = datetime.today().date()
        upcoming_birthdays = []
        for record in self.data.values():
            if record.birthday is None:
                continue
            next_birthday = self.get_next_birthday(today, record.birthday.value)
            if (next_birthday - today).days <= birthday_days:
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