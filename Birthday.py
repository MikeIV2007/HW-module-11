import datetime
import calendar
from rich import print
from rich.table import Table

def find_next_monday()->datetime:
    
    current_datetime = datetime.datetime.now()
    some_day = current_datetime.date() # actual value
    #some_day = datetime.date(year=2023, month=12, day=25) #- to test end of the year
    #some_day = datetime.date(year=2020, month=2, day=26) #- to test and of month and leap year period

    week_day = calendar.weekday(some_day.year, some_day.month, some_day.day)

    if week_day == 0:
        next_monday = some_day + datetime.timedelta(days=7)
        return next_monday
    
    else:
        for i in range (7):
            
            some_day = some_day + datetime.timedelta(days=1)
            week_day = calendar.weekday(some_day.year, some_day.month, some_day.day)

            if week_day == 0:
                next_monday = some_day
                return next_monday
            else:
                continue


def one_week_range(next_monday: datetime) -> datetime:

    start_of_range = next_monday - datetime.timedelta(days=2) 
    end_of_range = next_monday + datetime.timedelta(days=4)

    return start_of_range, end_of_range

def birthday_dict_in_range(range: datetime, colleagues_dict: dict) -> dict:
    birthday_dict = {}

    for name, birthday in colleagues_dict.items():
    
        if range[0].month == 12 and range[1].month == 1:

            if birthday.month == 12:
                birthday_year_12 = range[0].year
                birthday_12 = datetime.date(birthday_year_12, birthday.month, birthday.day)
                if range[0] <=  birthday_12 <= range[1]:
                    birthday_dict[name] = birthday

            if birthday.month == 1:
                birthday_year_1 = range[1].year
                birthday_1 = datetime.date(birthday_year_1, birthday.month, birthday.day)

                if range[0] <=  birthday_1 <= range[1]:
                    birthday_dict[name] = birthday
            
        else:
            if range[0].month <=  birthday.month <= range[1].month:
                birthday_to_range = datetime.date(range[0].year, birthday.month, birthday.day) 
                
                if range[0] <=  birthday_to_range <= range[1]:
                    birthday_dict[name] = birthday

    return birthday_dict

def table_rows_list (birthday_dict: dict, range: datetime) ->list:
    list_to_print=[]
    i = 1
    for name, birthday in birthday_dict.items():

        if range[0].month == 12 and range[1].month == 1:
            if birthday.month == 12:
                year = range[0].year
                value_12 = datetime.date(year, birthday.month, birthday.day)
                day_of_week = calendar.weekday(year, birthday.month, birthday.day)

                if day_of_week  == 5 or day_of_week ==6:
                    day_of_week = 0
                lst = [day_of_week, name, birthday]
                list_to_print.append(lst)

            if birthday.month == 1:
                year = range[1].year
                value_1 = datetime.date(year, birthday.month, birthday.day)
                day_of_week = calendar.weekday(year, birthday.month, birthday.day)
                
                if day_of_week  == 5 or day_of_week ==6:
                    day_of_week = 0
                lst = [day_of_week, name, birthday]
                list_to_print.append(lst)
        else:
                      
            year = range[0].year
            day_of_week = calendar.weekday(year, birthday.month, birthday.day)
            if day_of_week  == 5 or day_of_week ==6:
                day_of_week = 0        
            lst = [day_of_week, name, birthday]
            list_to_print.append(lst)

    list_to_print.sort()
 
    return list_to_print


def print_table(list_to_print: list, range: datetime)-> print:

    table = Table(title=f"\nNEXT WEEK BERTHDAYS\nfrom {str(range[0])} to {str(range[1])}")
    table.add_column("Day of week", justify="left", style="magenta")
    table.add_column("Colleague Name", justify="left")
    table.add_column("Birthday", justify="center", style="magenta")
    a= b = c = d = e =1
    for i in list_to_print:
    
        if i[0] == 0:
            if a == 1:
                day_of_week = 'Monday'
                a += 1
            else:
                day_of_week = '' 

          
        if i[0] == 1:
            if b == 1:
                day_of_week = 'Tuesday'
                b += 1
            else:
                day_of_week = ''

        if i[0] == 2:
            if c == 1:
                day_of_week = 'Wednesday'
                c += 1
            else:
                day_of_week = ''

        if i[0] == 3:
            if d == 1:
                day_of_week = 'Thursday'
                d += 1
            else:
                day_of_week = ''

        if i[0] == 4:
            if e == 1:
                day_of_week = 'Friday'
                e += 1
            else:
                day_of_week = ''

        table.add_row(day_of_week, str(i[1]), str(i[2]))
        
    return print(table)


def get_birthdays_per_week (colleagues_dict: dict) -> None:

    calendar.setfirstweekday(calendar.MONDAY) #monday 0 - sundey 6
    next_monday = find_next_monday()
    range = one_week_range( next_monday)
    birthday_dict = birthday_dict_in_range(range, colleagues_dict)
    table_rows_lst = table_rows_list (birthday_dict, range)
    print_table (table_rows_lst, range)


if __name__ == '__main__':

    from faker import Faker 
    from faker.providers import profile

    fake = Faker() #("uk-UA")-ukrainian legguage
    fake.add_provider(profile)
    
    #Faker.seed(1) #1 for constant dict
    
    def create_test_colleagues_dict():
        colleagues_dict = {}

        for i in range(200):

            prof = fake.profile()
            birthday = prof['birthdate']
            colleagues_dict[prof['name']] = birthday
          
        return colleagues_dict
    
    colleagues_dict = create_test_colleagues_dict()

    get_birthdays_per_week (colleagues_dict)