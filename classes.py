from collections import UserDict
from datetime import datetime, timedelta
from typing import Any

class Field:
    def __init__(self, value) -> None:
        self.value = value
    
    def __str__(self) -> str:
        return self.value
    
    def __repr__(self) -> str:
        return str(self)
    
    # def __setattr__(self, __name: str, __value: Any) -> None:
    #     pass

    # def __getattribute__(self, __name: str) -> Any:
    #     pass
        

class Name(Field):
    ...
    

class Phone(Field):
    ...
    # def __init__(self, value, rooms=255):
    #     self.__name = None
    #     self.name = value
    
    # @property
    # def name(self):
    #     return self.__name.upper()
    
    # @name.setter
    # def name(self, value):
    #     if not isinstance(value, str):
    #         raise WrongHotelName("Name must be string")
    #     self.__name = value

class Birthday(Field):
    ...


class Record:
    def __init__(self, name: Name, phone: Phone = None, birthday: Birthday = None) -> None:
        self.name = name
        self.phones = []
        #if phone.value:
        if phone != None:
            self.phones.append(phone)
        self.birthday = birthday
    
    def add_phone(self, phone: Phone):
        if phone.value not in [p.value for p in self.phones]:
            self.phones.append(phone)
            return f"\nPhone number {phone} to contact {self.name} is added successfully!"
        return f"\nThe phone number {phone} for {self.name} is already in adress book!"
    
    # def change_phone(self, old_phone, new_phone):
    #     for idx, p in enumerate(self.phones):
    #         if old_phone.value == p.value:
    #             self.phones[idx] = new_phone
    #             return f"old phone {old_phone} change to {new_phone}"
    #     return f"{old_phone} not present in phones of contact {self.name}"

    def delete_pone(self, phone_to_delete):
        for phone in self.phones:
            if phone.value == phone_to_delete.value:
                self.phones.remove(phone)
                return f'\nPhone number {phone.value} for {self.name} removed successfully!'
        return f"{phone_to_delete} is not in the phones list of the contact {self.name}"
    
    def add_birthday(self, birthday: Birthday):
        print ('75', self.birthday)
        if self.birthday == None:
            self.birthday = birthday
            return f"\nBirthday {self.birthday} to contact {self.name} is added successfully!"
        return f"\nThe {birthday} for {self.name} is already in adress book!"
    
    def days_to_birthday(self):
        if self.birthday:
            date_now = datetime.now().date()
            #print ('date now',str(date_now))
            format_str = "%Y-%m-%d"
            birthday_datetime = datetime.strptime(str(self.birthday.value), format_str).date()
            #print ('birthday_datetime',birthday_datetime)
            #print (date_now.year)
            #print (birthday_datetime.month)
            #print (birthday_datetime.day)
            birthday_this_year = datetime(date_now.year, birthday_datetime.month, birthday_datetime.day).date()
            #print (f'birthday_this_year {birthday_this_year}')
            delta = (birthday_this_year - date_now).days
            #print (f'delta {delta}')
            if delta > 0:
                return f'\n{delta} days until the next birthday of {self.name}'
            elif delta == 0:
                return f'\n{self.name} birthday is today!'
            else:
                birthday_next_year = datetime(date_now.year + 1, birthday_datetime.month, birthday_datetime.day).date()
                delta = (birthday_next_year - date_now).days
                return f'\n{delta} days until the next birthday of {self.name}'
        

        else:
            return f'\nBirthday for {self.name} is unknown!'
        
    def __str__(self) -> str:
        print ('110', len(self.phones))
        if len(self.phones) <= 1:
            return f"{self.name}; Unknown; {self.birthday}"
        return f"{self.name}; {', '.join(str(p) for p in self.phones)}; {self.birthday}"


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[str(record.name)] = record
        return f"\nContact {record} added successfully!"

    def __str__(self) -> str:
        return "\n".join(str(r) for r in self.data.values())
    
if __name__ == '__main__':

    """    # Bill +380(67)333-43-54
    #     name_1 = Name('Bill')
    #     print ('123', name_1)
    #     phone_1 = Phone('+380(67)333-43-54')
        #phone_1 = Phone(None)
        #print ('125', phone_1)
    #     #birthday = Birthday('2000-12-15')
    #    #birthday = Birthday('2000-07-18')
    #     birthday = Birthday('2000-07-17')
    #     print ('129', birthday)
    #     record_1 = Record(name_1, phone_1, birthday)
    #     print ('131', record_1)
    #     print ('132', record_1.birthday.value)
    #     address_book = AddressBook()
    #     address_book.add_record(record_1)
    #     print ('134', address_book)
    #     print ('135', record_1.days_to_birthday())"""
