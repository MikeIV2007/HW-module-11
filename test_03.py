class Field:
    def __init__(self, value) -> None:
        self.value = value
    
    def __str__(self) -> str:
        return self.value
    
    def __repr__(self) -> str:
        return str(self)
    # def __init__(self, value, rooms=255):
    #     self.__name = None
    #     self.name = value

class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)
        self.__value = None
        self.value = value


    @property
    def value(self):
        return f'I am getter {self.__value}'
    
    @value.setter
    def value(self, value):
        if not isinstance(value, str):
            #raise WrongHotelName("Name must be string")
            raise "Name must be string"
        self.__value = value


if __name__ == '__main__':
    # person  = Birthday('Karl')
    # print (person.birth)

    #name = Name ('bill')
    #birthday = Birthday('2000-12-15')
    birthday = Birthday('karl')
    #print (name)
    print ('41', birthday.value)
    print ('42', type(birthday))
    print ('43', str(birthday.value))