import sqlite3
from dateutil import parser


def store(table_name: str, entry_tuple: tuple[str]):
    conn = sqlite3.connect(f"hwoptdb.db")
    qstring = ("?," * (len(entry_tuple) - 1)) + "?"
    with conn:
        c = conn.cursor()
        c.execute(f"INSERT INTO {table_name} VALUES ({qstring})", entry_tuple)
    conn.close()


def insert_class():
    # gened_penalty = 5 / 8
    input_list = ["class name", "major or gened (m/g)", "total points"]
    entry = []
    go = 0
    i = 0

    print("\nProvide the following information (or hit Ctrl+C to exit)...")
    while i < len(input_list):
        inp = input(f" - {input_list[i]}: ")
        if inp == "q":
            break
        else:
            entry.append(inp)
            i += 1
            go = 1 if i == (len(input_list) - 1) else 0

    # attr_list[1] = 1 if attr_list[1] == "T" else gened_penalty
    if go == 1:
        store("classes", tuple(entry))


def insert_late_policy():
    entry_list = []
    deadline_count_pairs = []
    print("\nProvide the following information (or hit Ctrl+C to exit)...")
    policy_name = input(" - policy name: ")
    independent_deadlines_count = input(" - # of independent deadlines: ")

    for i in range(independent_deadlines_count):
        deadline_input = input(f"   - deadline {i}: ")
        try:
            # if you're giving a concrete date, let the parser interpret it and paste it in a nice format
            deadline = str(parser.parse(deadline_input))
        except parser.ParserError:
            # if it's not a concrete date, then I assume that it's a valid date variable...might be bad but idk
            deadline_input = deadline
        deadline_count = int(input(f"   - # of phases dependent on deadline {i}: "))
        deadline_count_pairs.append((deadline, deadline_count))
    
    total_value = 1
    for i in range(len(deadline_count_pairs)):
        for j in range(deadline_count_pairs[i][1]):
            
            hour_offset = 0
            if j != 0:
                hour_offset = print()
            if i == len(deadline_count_pairs) - 1 and j == deadline_count_pairs[i][1] - 1:
                
            

    """entry_list = []
    print("\nProvide the following information (or hit q to exit)...")
    policy_name = input(" - policy name: ")
    tip_count = input(" - turn-in phase count: ")
    i = 0
    while i < tip_count:
        deadline_offset = 0
        deadline_num = input(f" - deadline num (phase {i+1}): ")
        if i > 0 and deadline_num:
            deadline_offset = input(f" deadline offset (phase {i+1})")
        entry_list.append([policy_name, deadline_num, deadline_offset])"""

    """input_list1 = ["policy name", "turn-in phase count"]
    entry_list = []
    go = 1

    print("\nProvide the following information (or hit q to exit)...")
    policy_name = input(" - policy name: ")
    tip_count = input(" - turn-in phase count: ")

    i = 1
    total_pct_value = 1
    while i < tip_count:
        pct_value = input(
            f" - % deduction (from original grade) after phase {i}: "
        )
        total_pct_value -= pct_value
        deadline_scheme = input(f" - deadline scheme for phase {i+1}: ")
        entry_list.append(
            [
                policy_name,
                pct_value,
            ]
        )
    entry_list.insert(0, [policy_name, total_pct_value, "1|0"])"""


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
    print(" - (Ctrl+C) get me the hell outta here")
    return input()


def process_insert_input(pick: str):
    try:
        if pick == "1":
            insert_class()
        elif pick == "2":
            insert_late_policy()
        elif pick == "3":
            insert_assignment_template()
        elif pick == "4":
            insert_assignment()
    except KeyboardInterrupt:
        print()
        pass


def insert_loop():
    try:
        while True:
            process_insert_input(get_insert_input())
    except KeyboardInterrupt:
        pass


def generate_prindex_table():
    pass


def clean_deadlines():
    pass


def get_menu_input() -> str:
    print("\nhwopt welcomes you. What would you like to do with hwopt?")
    print(" - (1) Generate prindex")
    print(" - (2) Insert into hwopt")
    print(" - (Ctrl+C) Quit hwopt")
    return input()


def process_menu_input(pick: str) -> int:
    if pick == "1":
        generate_prindex_table()
    elif pick == "2":
        insert_loop()
    else:
        return 0
    return 1


def menu_loop():
    try:
        while True:
            process_menu_input(get_menu_input())
    except KeyboardInterrupt:
        pass


def bye_bye():
    print("\nhwopt says bye bye!")


def main():
    menu_loop()
    bye_bye()


if __name__ == "__main__":
    main()
