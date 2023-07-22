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

class Persons(Field):
    def __init__(self, value):
        super().__init__(value)
        self.__person = None
        self.person = value


    @property
    def person(self):
        #return self.__person.upper()
        return f'getter {self.__person}'
    @person.setter
    def person(self, value):
        if not isinstance(value, str):
            #raise WrongHotelName("Name must be string")
            raise "Name must be string"
        self.__person = value

person  = Persons('Karl')
print (person.person)