class Dog:
    def __init__(self, name, age):
        self.__name = name
        self.__age = age

    def getAge(self):
        return self.__age

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def set_age(self, a):
        self.__age = a

    def __str__(self):
        return "Dog ~\nName: " + self.__name + "\nAge: " + str(self.__age)


class Cat:
    def __init__(self, name, color, asshole):
        self.__name = name
        self.__color = color
        self.__asshole = asshole

    def __str__(self):
        return (
            "Cat ~\nName: "
            + self.__name
            + "\nColor: "
            + self.__color
            + "\nAsshole: "
            + str(self.__asshole)
        )
