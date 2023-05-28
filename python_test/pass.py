class I_Contain_Stuff:
    def __init__(self, my_float):
        self.my_float = my_float
        self.my_list = [1, 2, 3]


def i_change_stuff(input_float, input_list, input_str):
    bruh = input_float
    bruh2 = input_list

    bruh += 0.6
    bruh2 = bruh2.append(2)


def i_change_stuff_differently(input_container):
    bruh = input_container
    bruh.my_float += 0.6
    bruh.my_list = [4, 4]


Float_Container = I_Contain_Stuff(4.4)
print(f"Before either, Float_Container.my_float = {Float_Container.my_float}")
i_change_stuff(Float_Container.my_float)
print(
    f"After i_change_floats(), Float_Container.my_float = {Float_Container.my_float}"
)
i_change_stuff_differently(Float_Container)
print(
    f"After i_change_floats_differently(), Float_Container.my_float = {Float_Container.my_float}"
)
