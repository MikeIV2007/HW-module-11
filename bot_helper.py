import re
from rich import print
from rich.table import Table

from collections import UserDict

I = 1

class Field:
    pass


class Name(Field):
    def __init__(self, name) -> None:
        self.name = name


class Phone(Field):
    def __init__(self, phone):
        self.phone = phone


class Record(Field):
    def __init__(self, name, phone):
        self.name = name
        self.phone = phone
      
    def add_record(self):
        self.phones = []
        self.phones.append(self.phone)
        address_book.data[self.name] = self.phones
    
    def add_phone(self):
        phones_list = address_book.data[self.name]
        phones_list.append(self.phone)
        address_book.data[self.name] = phones_list

    def delete_phone(self):
        phones_list = address_book.data[self.name]
        phones_list.remove(self.phone)
        address_book.data[self.name] = phones_list 


class AddressBook(UserDict):

    def display_contacts(self):

        table = Table(title="\nALL CONTACTS IN DATABASE")
        table.add_column("Name", justify="left")
        table.add_column("Phone number", justify="left")

        if len(self.data) == 0:
            print ('\nAddress Book is empty!')
            return main()
        
        for name, phone_numbers in self.data.items():
            phones_str = ''
            for item in phone_numbers:
                phones_str += item.phone + ' '

            table.add_row(name.name, phones_str.strip())
        print (table)
        return main()

address_book = AddressBook()


def table_of_commands():

    table = Table(title="\nALL VALID COMMANDS:\n(All entered data must be devided by gap!)")
    table.add_column("COMMAND", justify="left")
    table.add_column("NAME", justify="left")
    table.add_column("PHONE NUMBER", justify="center")
    table.add_column("DESCRIPTION", justify="left")
    table.add_row('hello', '-', '-', 'Greeting')
    table.add_row('add', 'Any name ', 'Phone number in any format', 'Add new contact')
    table.add_row('append', 'Existing name', 'Additional phone number', 'Append phone number') 
    table.add_row('delete', 'Existing name', 'Phone to delete', 'Delete phone number')
    table.add_row('phone', 'Existing name', '-', 'Getting phone number')
    table.add_row('show all', '-', '-', 'Getting all database')
    table.add_row('good bye / close / exit', '-', '-', 'Exit')
    table.add_row('help', '-', '-', 'Printing table of commands')

    return print (table)


def user_name_exists(func):

    def wrapper(user_name: str, phone_number: str):

        for name, phone  in address_book.data.items():
            if user_name == name.name:
                func(user_name, phone_number)

        print (f'\nContact {user_name} is not exist! Try other options!')
        return main()
  
    return wrapper


def hello():
    print('\nHow can I help you?')
    return main()


def exit_programm():
    print ('\nGood bye! Have a nice day!\n')
    exit()


def add(user_name, phone_number):

    name = Name(user_name)
    phone = Phone(phone_number)
    record = Record(name, phone)

    for name, phone in address_book.data.items():
        if name.name == user_name:
            print (f'\nContat {name.name} is already exist! Try other options!')
            return main()
    if phone_number == '':
        print ('There is no phone number')
        return main()
    record.add_record()
    print (f'\nNew contat {user_name} {phone_number} added successfully!')
    return main()

@user_name_exists
def delete(user_name: str, phone_number:str):
    for name, phones in address_book.data.items():
        if name.name == user_name:
            for item in phones:
                if phone_number == item.phone:
                    delete_record = Record (name, item)
                    delete_record.delete_phone()
                    print (f'\nPhone number {item.phone} for {name.name} removed successfully!')
                    return main()
                else:
                    print (f'Phone {phone_number} for {user_name} was not found!')
                    return main


@user_name_exists
def phone(user_name:str, phone_number: str):
    for name, phones in address_book.data.items():
        if name.name == user_name:
            phones_str = ''
            for item in phones:
                phones_str += item.phone + ' '
            print (f'\nPhone number of {name.name} is: {phones_str}')
            return main()


@user_name_exists
def append(user_name:str, phone_number: str):

    for name, phones in address_book.data.items():

        if name.name == user_name:
            additional_phone = Phone(phone_number)
            additional_record = Record (name, additional_phone )
            additional_record.add_phone()
    
    print (f'\nAdditional phone number {phone_number} for {name.name} saved successfully')
    return main()

def show_all():
    address_book.display_contacts()
    

COMMAND_INPUT = {'hello': hello, 
                'add': add,
                'show all': show_all,
                'exit': exit_programm,
                'good bye': exit_programm, 
                'close': exit_programm,
                'help': table_of_commands,
                'delete': delete,  
                'phone': phone,
                'append': append}


def execute_command(command, user_name, phone_number):
    COMMAND_INPUT[command](user_name, phone_number)


def input_error(func):
    def wrapper(data:str):
        try:
            regex_command = r'^[a-zA-Z]+'
            match = re.search(regex_command, data)
            
            if match:
                command = (match.group()).lower()

            if command in COMMAND_INPUT:
                span = match.span()
                user_info = data[span[1]:].strip()
                return command, user_info
            
            else:
                print ('\nUnknown command! Try agayn!')
                return main()
                
        except(KeyError, ValueError, IndexError, TypeError, UnboundLocalError):
            print ('\nWrong input! Try again')
            return main()
    return wrapper


def check_phone_number(command, phone):
    if command == 'phone':
        return phone
    if 18>= len(phone) >= 10:
        for i in phone:
            if i in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '-', '(', ')', ' '):
                continue
            else:
                print (f'Phone number {phone} is not correct')
                return main()
            
        return phone
    else:
        print (f'Phone number {phone} is not valid! It must be in range from 10 to 18 characters! Try againe!')
        return main()


def get_user_name(command: str, user_info: str )-> tuple:

    regex_name = r'[a-zA-ZА-Яа-я]+'
    user_input_split = user_info.strip().split()
    name_list =[]
    for i in user_input_split:
        match_name = re.match(regex_name, i)
        if match_name:
            if len(match_name.group()) == len(i):
                name_list.append(i.capitalize())
                user_info = user_info[match_name.span()[1]:].strip()
                phone = user_info
            else:
                print ('\nName is not correct! Try again!')
                return main()

    if len(name_list)>=1:
        name = ' '.join(name_list)
        
    else:
        print ('\nName is not correct! Try again!')
        return main()
    
    return name, phone


@input_error
def identify_command_get_info(input: str):

    regex_command = r'^[a-zA-Z]+'
    match = re.search(regex_command, input)
    
    if match:
        command = (match.group()).lower()

        if command in COMMAND_INPUT:
            span = match.span()
            user_info = input[span[1]:].strip()
            return command, user_info
        
    else:
        print ('\nUnknown command! Try agayn!')
        return main()
          
        
def get_user_input():

    global I
    
    if I == 1:
        table_of_commands()
        I += 1

    while True:
        user_input = (input(f'\nEnter command, please!\n\n>>>')).strip()

        if user_input.lower() == "hello":
            return COMMAND_INPUT[user_input]()
          
        if user_input.lower() == 'show all':
            return COMMAND_INPUT[user_input]()                  

        if user_input.lower() in  ('exit', 'close', 'good bye'):
            return COMMAND_INPUT[user_input]()
        
        if user_input.lower() == 'help':
            return COMMAND_INPUT[user_input](), main() 

        return user_input
    

def main():

    user_input = get_user_input()
    command, user_info = identify_command_get_info(user_input )
    name, phone = get_user_name(command, user_info)
    phone = check_phone_number(command, phone)
    execute_command(command, name, phone)

    
if __name__ == "__main__":
    main()

# 
# ADD Bill +380(67)333-43-54
# Append Bill +380(67)333-11-11
# phone Bill
# DeLete Bill +380(67)333-43-54
# ADD Bill Jonson +380(67)333-43-5
# Append Bill Jonson +380(67)333-99-88
# PhoNE Bill Jonson
# DeleTe Bill Jonson +380(67)333-43-5
# +380(67)282-8-313
# CHange Mike Jonn +380(67)111-41-77
# delete Mike Jonn +380(67)111-41-77
# PHONE Mike Jonn +380(67)111-41-77
# CHange Bill Jonson +380(67)111-41-77
# PHONE Bill
# phone Bill +380(67)333-43-54
# 12m3m4n
# 12me3m3m 123m3mm2
# ADD Jill Bonson +380(67)333-43-54
# PhOnE Jill Bonson +380(67)333-43-54
# ADD Jill +380(67)333-43-54
# append Jill +380(67)222-44-55
# Иванов Иван Иванович +380(67)222-33-55
# append Иванов Иван Иванович +380(67)999-1-777
# phone Иванов Иван Иванович 
# delete Иванов Иван Иванович +380(67)222-33-55
# dfsadfads asdgfas ref asdf     TypeError
# Jgfdksaflf Sdfjldsf; Asdfk;;lsdff Jldsf;sf';; sdff ; jldsf;sF';;
# add mike 123123-12-3
# delete mike 123123-12-3
# phone mike 123123-12-3