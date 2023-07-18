"""У цьому домашньому завданні ми:

Додамо поле для дня народження Birthday. Це поле не обов'язкове, але може бути тільки одне. DONE
Додамо функціонал роботи з Birthday у клас Record, а саме функцію days_to_birthday, яка повертає кількість днів до наступного дня народження.DONE
Додамо функціонал перевірки на правильність наведених значень для полів Phone, Birthday.
Додамо пагінацію (посторінкове виведення) для AddressBook для ситуацій, коли книга дуже велика і потрібно показати вміст частинами, а не все одразу. Реалізуємо це через створення ітератора за записами.
Критерії приймання:
AddressBook реалізує метод iterator, який повертає генератор за записами AddressBook і за одну ітерацію повертає представлення для N записів.
Клас Record приймає ще один додатковий (опціональний) аргумент класу Birthday
Клас Record реалізує метод days_to_birthday, який повертає кількість днів до наступного дня народження контакту, якщо день народження заданий.
setter та getter логіку для атрибутів value спадкоємців Field.
Перевірку на коректність веденого номера телефону setter для value класу Phone.
Перевірку на коректність веденого дня народження setter для value класу Birthday."""


import re
from rich import print
from rich.table import Table
from classes import AddressBook, Name, Phone, Record, Birthday

address_book = AddressBook()

def table_of_commands():
    table = Table(title='\nALL VALID COMMANDS:\n(All entered data must be devided by gap!)')
    table.add_column('COMMAND', justify='left')
    table.add_column('NAME', justify='left')
    table.add_column('PHONE NUMBER', justify='center')
    table.add_column('DESCRIPTION', justify='left')
    table.add_row('hello', '-', '-', 'Greeting')
    table.add_row('add', 'Any name ', 'Phone number in any format', 'Add new contact')
    table.add_row('append', 'Existing name', 'Additional phone number', 'Append phone number') 
    table.add_row('delete', 'Existing name', 'Phone to delete', 'Delete phone number')
    table.add_row('phone', 'Existing name', '-', 'Getting phone number')
    table.add_row('show all', '-', '-', 'Getting all database')
    table.add_row('good bye / close / exit', '-', '-', 'Exit')
    table.add_row('help', '-', '-', 'Printing table of commands')

    return table


def input_error(func):
    def wrapper(*args):
        try:
            return func(*args)
        
        except IndexError as e:
            error_message = f"IndexError: {str(e)}"
            return error_message
    return wrapper


@input_error
def add_command(*args):

    name = Name(args[0])
    phone = Phone(args[1])
    birthday = Birthday([3])
    rec: Record = address_book.get(str(name))

    if rec:
        return rec.add_phone(phone)
    rec = Record(name, phone, birthday)
    return address_book.add_record(rec)


def delete_phone_command(*args):

    name = Name(args[0])
    phone_to_delete = Phone (args[1])
    record: Record = address_book.get(str(name))

    if record:
        return record.delete_pone(phone_to_delete)
    return f'\nContact {name} in address book is not found!'


def phone_command(*args):

    for name, record in address_book.data.items():
        if name == args[0]:
            phones = ", ".join(str(phone) for phone in record.phones)
            return (f'\nPhone number(s) of {name} is: {phones}')
        
    return f'\nContact {name} in address book is not found!'


def exit_command(*args):
    return '\nGood bye! Have a nice day!\n'


def show_all_command(*args):

    table = Table(title='\nALL CONTACTS IN DATABASE')
    table.add_column('Name', justify='left')
    table.add_column("Phone number", justify="left")

    if len(address_book.data) == 0:
        return '\nAddress Book is empty!'
    
    for name, record in address_book.data.items():
        phones_str = ''
        user_name = record.name
        user_phones_list = record.phones
        for item in user_phones_list:
            phones_str += item.value + ', '

        table.add_row(user_name.value, phones_str.strip())
    return table


def help_command(*args):
    return table_of_commands()


def hello_command(*args):
    return '\nHow can I help you?'

def days_to_birthday_command(*args):
    ...
    


COMMANDS = {
    add_command: ('add', 'append'),
    phone_command: ('phone',),
    delete_phone_command: ('delete',),
    exit_command: ('good bye', 'close', 'exit'),
    show_all_command: ('show all',),
    help_command: ('help',),
    hello_command: ('hello',)
}

def check_phone_number(command, phone):
    if command == 'phone':
        return phone
    if 18>= len(phone) >= 10:
        for i in phone:
            if i in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '-', '(', ')', ' '):
                continue
            else:
                return (f'Phone number {phone} is not correct')
      
        return phone
    else:
        return (f'Phone number {phone} is not valid! It must be in range from 10 to 18 characters! Try againe!')



def get_user_name(user_info: str )-> tuple:

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
                return '\nName is not correct! Try again!'


    if len(name_list)>=1:
        name = ' '.join(name_list)
    else:
        name = ''
        phone = ''

    return name, phone

def parser(text:str):
    for command, kwds in COMMANDS.items():
        for kwd in kwds:
            if text.lower().startswith(kwd):
                user_info = text[len(kwd):].strip()
                return command, user_info
            
    print ('\nUnknown command! Try againe!')
    command = None
    user_info = None
    return command, user_info


def main():

    #print (table_of_commands())

    while True:
        user_input = (input(f'\nEnter command, please!\n\n>>>')).strip()
        
        command, user_info = parser(user_input)
        if user_info or command:
            name, phone = get_user_name(user_info)
            phone = check_phone_number(command, phone)
            data = (name, phone)
            result = command(*data)
            print(result)
        
        if command == exit_command:
            break

if __name__ == "__main__":
    main()

# 
# show all
# help
# phone
# ADD Bill
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