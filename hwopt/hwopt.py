import sqlite3


def store(table_name: str, attr_list: list[str]):
    conn = sqlite3.connect(f"hwoptdb.db")
    qstring = ("?," * (len(attr_list) - 1)) + "?"
    with conn:
        c = conn.cursor()
        c.execute(f"INSERT INTO ? VALUES ({qstring})", (table_name, *attr_list))
    conn.close()


def insert_class():
    gened_penalty = 5 / 8
    input_list = ["class name", "major class (T/F)", "total points"]
    attr_list = []
    inp = ""
    i = 0

    print("Provide the following attributes (or hit q to exit):")
    while inp != "q" and i < len(input_list):
        attr_list.append(input(f" - {input_list[i]}:"))
        i += 1

    attr_list[1] = 1 if attr_list[1] == "T" else gened_penalty
    store("classes", attr_list)


def insert_late_policy():
    pass


def insert_assignment_template():
    pass


def insert_assignment():
    pass


def get_insert_input() -> str:
    print("\nWhat would you like to insert?")
    print(" - (1) Class")
    print(" - (2) Late Policy")
    print(" - (3) Assignment Template")
    print(" - (4) Assignment")
    print(" - (q) Go back to main menu")
    print("")

    return input()


def process_insert_input(pick: str):
    if pick == 1:
        insert_class()
    elif pick == 2:
        insert_late_policy()
    elif pick == 3:
        insert_assignment_template()
    elif pick == 4:
        insert_assignment()


def insert():
    process_insert_input(get_insert_input())


def generate_prindex_table():
    pass


def clean_deadlines():
    pass


def get_menu_input() -> str:
    print("\nhwopt welcomes you. What would you like to do with hwopt?")
    print(" - (1) Generate prindex")
    print(" - (2) Insert into hwopt")
    print(" - (q) Quit hwopt")
    return input()


def process_menu_input(pick: str) -> int:
    if pick == "1":
        generate_prindex_table()
    elif pick == "2":
        insert()
    else:
        return 0

    return 1


def menu():
    return process_menu_input(get_menu_input())


def bye_bye():
    print("\nhwopt says bye bye!\n")


def menu_loop():
    go = 1
    while go == 1:
        go = menu()


def main():
    menu_loop()
    bye_bye()


if __name__ == "__main__":
    main()
