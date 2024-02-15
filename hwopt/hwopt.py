import sqlite3
from decimal import Decimal
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
        entry = tuple(entry)
        print(f"Inserting {entry}...")
        store("classes", entry)
        print("Done!")


def insert_late_policy():
    # init
    entry_list = []
    deadline_count_pairs = []
    prev_deduct = Decimal(0)

    # input
    print("\nProvide the following information (or hit Ctrl+C to exit)...")
    policy_name = input(" - policy name: ")
    independent_deadlines_count = int(input(" - # of independent deadlines: "))
    for i in range(independent_deadlines_count):
        deadline = input(f"   - deadline {i+1}: ")
        try:
            # if you're giving a concrete date, let the parser interpret it and paste it in a nice format
            deadline = str(parser.parse(deadline))
        except parser.ParserError:
            # if it's not a concrete date, then I assume that it's a valid date variable...might be bad but idk
            pass
        deadline_count = int(
            input(f"   - # of phases dependent on deadline {i+1}: ")
        )
        deadline_count_pairs.append((deadline, deadline_count))
    for i in range(len(deadline_count_pairs)):
        # for formatting
        if i != 1 and deadline_count_pairs[i][1] > 1:
            print(f" - {deadline_count_pairs[i][0]} -")
        for j in range(deadline_count_pairs[i][1]):
            deduct = 1
            hour_offset = 0
            if j != 0:
                hour_offset = int(input(f"   - hour offset {j}: "))
            if (
                i != len(deadline_count_pairs) - 1
                or j != deadline_count_pairs[i][1] - 1
            ):
                deduct = Decimal(input(f"   - pct deduction {j+1}: ")) / 100

            entry_list.append(
                (
                    policy_name,
                    str(deduct - prev_deduct),
                    deadline_count_pairs[i][0],
                    hour_offset,
                )
            )
            prev_deduct = deduct

    # storing in table
    for i in range(len(entry_list)):
        print(f"Inserting {entry_list[i]}...")
        # could have used c.executemany() for this, btw
        store("lp_template_phases", entry_list[i])
    print("Done!")


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
