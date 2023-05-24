from Dog_Cat import Dog, Cat

d1 = Dog("Scruffy", 5)
# Dog.__init__(d1, "Ruffly", 3)
# d1.__init__("Scrumfly", 6)
d1.set_age(10)  # implicit self pass

c1 = Cat("florence", "black", True)

"""
this is something you can't do in java: use class A's (Dog's) setter method to 
change the fields of an instance of class B (Cat). Note that this only works 
if Cat's name field ISN'T name-mangled (AKA it doesn't have a dunderscore)
"""
Dog.set_name(c1, "rugby")

"""
using a foreign setter that doesn't happen to use an identically-named field
just results in a silent ignore as opposed to a run-time error; we don't need 
name-mangling to achieve this here tho
"""
Dog.set_age(c1, 12)

"""
Setting c1's dunderscored variable to False doesn't change c1's actual asshole 
field because of the dunderscore.
"""
c1.__asshole = False
print(c1.__asshole)  # prints False, but c1's actual field is still True

print(d1)
print(c1)
