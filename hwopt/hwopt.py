import sqlite3
from decimal import Decimal
from dateutil import parser


def connect_to_db() -> sqlite3.Connection:
    conn = sqlite3.connect(f"hwopt.db")
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def store(table_name: str, entry_tuple_list: list[tuple[str]]):
    conn = connect_to_db()
    # makes assumption that that all members of entry_tuple_list have exactly as many elements as entry_tuple_list[0] does...
    qstring = ("?," * (len(entry_tuple_list[0]) - 1)) + "?"
    with conn:
        c = conn.cursor()
        print("Inserting shit...")
        c.executemany(
            f"INSERT OR IGNORE INTO {table_name} VALUES ({qstring})",
            entry_tuple_list,
        )
        # OR IGNORE makes sure that we don't crash if user enters an entry that duplicates another entry's primary key (sqlite just doesn't enter it)
    conn.close()
    print("Done!")


# simpsing = simple + single
def get_simpsing_input(question_list: list[str]) -> tuple[str]:
    answer_list = []

    print("\nProvide the following information (or hit Ctrl+C to exit)...")
    for i in range(len(question_list)):
        inp = input(f" - {question_list[i]}: ")
        answer_list.append(inp)

    return tuple(answer_list)


def insert_class():
    question_list = ["class name", "major or gened (m/g)", "total points"]
    entry = get_simpsing_input(question_list)
    store("classes", [entry])


def insert_late_policy():
    # init
    phase_list = []
    deadvar_list = []
    deadline_count_pairs = []
    prev_deduct = Decimal(0)

    # input
    varcount = 0
    print("\nProvide the following information (or hit Ctrl+C to exit)...")
    policy_name = input(" - policy name: ")
    independent_deadlines_count = int(input(" - # of independent deadlines: "))
    for i in range(independent_deadlines_count):
        deadvar = input(f"   - deadline variable {i+1}: ")
        try:
            # if you're giving a concrete date, let the parser interpret it and paste it in a nice format
            deadvar = str(parser.parse(deadvar))
        except parser.ParserError:
            # if user does not provide a concrete date, then their input is taken to be a variable
            deadvar = f"x{varcount}"
            varcount += 1
        deadvar_list.append((policy_name, deadvar))
        deadline_count = int(
            input(f"   - # of phases dependent on {deadvar}: ")
        )
        deadline_count_pairs.append((deadvar, deadline_count))
    for i in range(len(deadline_count_pairs)):
        # for formatting
        if i != 1 and deadline_count_pairs[i][1] > 1:
            print(f" - {deadline_count_pairs[i][0]} -")
        for j in range(deadline_count_pairs[i][1]):
            deduct = Decimal(1)
            hour_offset = 0
            if j != 0:
                hour_offset = int(input(f"   - hour offset {j}: "))
            if (
                i != len(deadline_count_pairs) - 1
                or j != deadline_count_pairs[i][1] - 1
            ):
                deduct = Decimal(
                    input(f"   - pct deduction {j+1} (from original grade): ")
                ) / Decimal(100)
                # print(f"deduct is {str(deduct)}")
                # print(f"difference is {str(deduct - prev_deduct)}")

            phase_list.append(
                (
                    policy_name,
                    str(deduct - prev_deduct),
                    deadline_count_pairs[i][0],
                    hour_offset,
                )
            )
            prev_deduct = deduct

    store("lp_templates", [(policy_name,)])  # <- comma is necessary!!
    store("lp_template_deadvars", deadvar_list)
    store("lp_template_deadvar_phases", phase_list)


def null_sieve(input_str: str):
    return None if input_str == "n/a" else input_str


def insert_assignment_template():
    print("\nProvide the following information (or hit Ctrl+C to exit)...")
    format_str = " - "

    assignment_type = input(f"{format_str}assignment type: ")
    class_name = input(f"{format_str}class name: ")
    points = null_sieve(input(f"{format_str}points: "))
    # parse fractions jic
    if points is not None and "/" in points:
        split_frac = points.split("/")
        points = str(Decimal(int(split_frac[0])) / Decimal(int(split_frac[1])))
    late_policy = null_sieve(input(f"{format_str}late policy: "))

    store(
        "assignment_templates",
        [(assignment_type, class_name, points, late_policy)],
    )


def insert_assignment():
    print("\nProvide the following information (or hit Ctrl+C to exit)...")
    format_str = " - "
    conn = connect_to_db()

    assignment_name = input(f"{format_str}assignment name: ")
    class_name = input(f"{format_str}class name: ")
    template = null_sieve(input(f"{format_str}template: "))
    points = None
    late_policy = None

    if template is None:
        points = int(input(f"{format_str}points: "))
        late_policy = input(f"{format_str}late policy: ")
        lp_to_search = late_policy
    else:
        with conn:
            c = conn.cursor()
            c.execute(
                "SELECT points, late_policy_name FROM assignment_templates WHERE assignment_type = ? AND class_name = ?",
                (template, class_name),
            )
            template_excerpt = c.fetchone()
        if template_excerpt[0] is None:
            points = int(input(f"{format_str}points: "))
        if template_excerpt[1] is None:
            late_policy = input(f"{format_str}late policy: ")
            lp_to_search = late_policy
        else:
            lp_to_search = template_excerpt[1]

    with conn:
        c = conn.cursor()
        c.execute(
            """
            SELECT DISTINCT deadline_variable 
            FROM lp_template_deadvar_phases
            WHERE late_policy_name = ? AND deadline_variable LIKE '%%x%%'
            """,
            (lp_to_search,),
        )
        distinct_deadvars = c.fetchall()
    conn.close()

    deadvar_map_entries = []
    print(f"{format_str}deadlines{format_str}")
    for i in range(len(distinct_deadvars)):
        var_to_inspect = distinct_deadvars[i][0]
        deadvar_instance = var_to_inspect
        deadvar_instance = str(
            parser.parse(input(f"  {format_str}instance of {var_to_inspect}: "))
        )
        deadvar_map_entries.append(
            (assignment_name, class_name, var_to_inspect, deadvar_instance)
        )

    store(
        "assignments",
        [(assignment_name, class_name, points, late_policy, template)],
    )
    store("deadvar_maps", deadvar_map_entries)


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
