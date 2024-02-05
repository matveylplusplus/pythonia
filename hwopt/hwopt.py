import pandas as pd
from dateutil import parser
import datetime
import numpy


def gen_hwopt():
    """
    def print_hwopt():
        print("How would you like to sort hwopt?")
        print("(1) Prindex")
        print("(2) C-Prindex")
        pick = input()

        if pick == "1":
            hw.sort_values(["Prindex"], ascending=False)
        else:
            hw.sort_values(["C-Prindex"], ascending=False)

        return 1
    """


def gaze():
    go = 1
    while go == 1:
        inp = input(
            "\nEnter the name of the orfice which you would like to gaze into,"
            + " or hit q to quit: "
        )
        if inp == "q":
            go = 0
        else:
            df = pd.read_csv(f"{inp}.csv")
            print(df.to_string())


def insert():
    def insert_lp():
        # Init
        tipdf = pd.read_csv("tip.csv")
        tip_list = []
        dl_list = ["x1"]

        # Input
        lp_name = input("\nProvide a name for your late policy: ")
        tip_count = int(
            input("\nProvide the number of turn-in phases (tips): ")
        )
        print(
            "\n Provide the percent deductions, from the original grade, for each "
            + "late tip: "
        )
        for i in range(2, tip_count + 1):
            tip_list.append((float(input(f" - Phase {i}: "))) / 100)
        print(
            "\nProvide the datetime vars for each late phase, where x1 is the "
            + "original due date of the assignment: "
        )
        for i in range(2, tip_count + 1):
            dl_list.append(input(f" - Phase {i}: "))

        # Process
        tip_list = [0.0] + tip_list + [1.0]
        dlpct_list = numpy.diff(tip_list)

        # Write
        for i in range(0, len(dlpct_list)):
            tipdf.loc[len(tipdf.index)] = [
                lp_name,
                i + 1,
                dlpct_list[i],
                dl_list[i],
            ]

        tipdf.to_csv("tip.csv", index=False)

    def insert_class():
        # init
        classdf = pd.read_csv("class.csv")
        total_pts = "n/a"

        # input
        class_name = input("\nProvide the name of your class: ")
        maj = input("\nIs this class a major class (y/n)? ")
        pts_given = input(
            "\nDoes the syllabus provide a total point count (y/n)? "
        )
        if pts_given == "y":
            total_pts = int(input("What is it? "))

        # write
        classdf.loc[len(classdf.index)] = [class_name, maj, total_pts]
        classdf.to_csv("class.csv", index=False)

    def insert_type():
        # init
        typedf = pd.read_csv("type.csv")
        classdf = pd.read_csv("class.csv")
        pct = 0

        # input 1
        classname = input("\nTo which class does your assignment type belong? ")

        # process
        totalpts = classdf.loc[classdf["class_name"] == classname].iloc[0][
            "total_pts"
        ]

        # input 2
        typename = input("\nProvide the name of your type: ")
        if totalpts == "n/a":
            # can enter 'man' here for manual
            pct = input(
                f"\nWhat percentage of your grade does {typename} take up? "
            )
        else:
            typepts = int(input("\nHow many points is your type worth? "))
            tcount = int(
                input(
                    "\nHow many assignments of this type are there "
                    + "expected to be throughout the whole course? "
                )
            )
            # process pct
            pct = typepts / (int(totalpts) * tcount)
        lp = input(
            "\nProvide the name of the late policy that this assignment type "
            + "will be using: "
        )

        # write
        typedf.loc[len(typedf.index)] = [classname, typename, pct, lp]
        typedf.to_csv("type.csv", index=False)

    def insert_hw():
        # init
        hwdf = pd.read_csv("hw.csv")

        # input
        classname = input("\nProvide the assignment's class: ")
        typename = input("\nProvide the assignment's type: ")
        id = input("\nProvide an ID for your assignment: ")

        # write
        hwdf.loc[len(hwdf.index)] = [classname, typename, id]
        hwdf.to_csv("hw.csv", index=False)

    """
    def insert_hw():
        cl = input("For which class? ")
        name = input("With what name? ")
        dl = input("With what deadline ([month] [day] [time] [am/pm])? ")
        print(
            "Rank the difficulty of doing the assignment while commuting from "
            + "1-5, where:"
        )
        print(" - 1 = I may as well be at home")
        print(" - 2 = slightly harder")
        print(" - 3 = significantly harder")
        print(" - 4 = much much harder")
        print(" - 5 = impossible")
        print()
        com_factor = input()

        diff = parser.parse(dl) - datetime.datetime.now()
        print(f"In minutes, that's {int(diff.total_seconds()/60)}")

        late_days = 1
        daily_pct_cut = 0.1

        x = 0
        prindex_total = 0
        while x < late_days:
            prindex_total += (daily_pct_cut * pct) / dl
        prindex_total += ((1 - (daily_pct_cut * late_days)) * pct) / dl
        prindex_total *= com_factor * major_factor

        def get_prindex(m, c, p, t):
            return m * c * (p / t)

        def get_commute_factor(c):
            carr = [0, 0.25, 0.5, 0.75, 1]
            return carr[c - 1]
    """
    print("\nWhat would you like to insert?")
    print(" - (1) Late Policy")
    print(" - (2) Class")
    print(" - (3) Assignment-Type")
    print(" - (4) Assignment")
    pick = int(input(""))

    if pick == 1:
        insert_lp()
    elif pick == 2:
        insert_class()
    elif pick == 3:
        insert_type()
    elif pick == 4:
        insert_hw()


def main():
    print("\nhwopt welcomes you. What would you like to do with hwopt?")
    print(" - (1) Generate prindex")
    print(" - (2) Gaze into hwopt")
    print(" - (3) Insert into hwopt")
    print(" - (q) Quit hwopt")
    pick = input()

    toret = 1
    if pick == "1":
        gen_hwopt()
    elif pick == "2":
        gaze()
    elif pick == "3":
        insert()
    else:
        toret = 0

    return toret


# Start
go = 1
while go == 1:
    go = main()
print("\nhwopt says bye bye!\n")
# End

"""
Notes

To do:
    - insert()
        - write to csv files
        - Generates:
            - mpc (hw.csv)
            - P_1, ... , P_n (dl.csv), where P_n = P_1 + ... + P_{n-1}
            - dl_1, ... , dl_n (dl.scv)
    - gaze()
        - rows gaze() should append to hw.csv in a new dataframe that is
          displayed to user:
            - cum_prindex
            - cum_c-prindex / cum_cprindex
        - Generates:
            - datetime.now() -> dl - datetime.now() (denominators of prindexes
              in dl.csv)
    - remove()
    - implement update()
    - implement accounting for extra credit and HW drop

the problem with pre-computing mp is that percentages may change based on
unforeseen circumstances
    - eg "we dropped an exam because it was too hard" when you already have the 
    following exam loaded into hw.csv whose mp was calculated based on the
    assumption that each exam was worth 15% of your grade whereas now it's worth
    like 30% or something
    - does this actually happen though? I can't remember a single time in UMD 
    when an assignment was straight up *dropped* as opposed to curved
    - actually there was that one time with Stefan cuz I got sick
    - but if it does happen you can just re-enter the handful of assignments
    that were affected by this change?
    - I think we have 2 reasonable options:
        - just leave as much computation to gen()'s runtime as possible, greatly increasing
          adaptability for little dev time, at the expense of performance (how
          much? who knows)
        - leave as little computation to gen()'s runtime as possible (ie
          pre-load basically all the data except datetime.now()), but 
        implement an update() function where the user changes an attribute and
        then all entries (in all tables) that are contingent on that attribute
          as well as the pre-loads get updated accordingly. Greatly increases
          adaptability and (maybe?) performance, at the expense of dev time 

How to account for HW drops? Extra credit?
    - HW drops have to be accounted for on the user end lest we expand this 
    project to also contain a complete database of your grades, which would suck
    - So if you have 9 CMSC351 HWs done with the lowest grade being an 80%, you
    should put in HW10 exactly the same way you normally would except with 
    respect to the points (CMSC351 HWs are out of 100 pts): instead of standing
    to gain 100 pts from this assignment, you stand to gain 20, because the
    lowest 2 HWs are dropped! 
    - But this can't be right because this is a no-lose situation. The whole 
    idea of the program is that your grade starts at 100% and you're trying to 
    gauge which assignments will pull your grade down the most if you don't do
    them. In this mental model, the idea of HW drops throws everything out of
    wack because now how "far" your grade is pulled down if you don't do a HW 
    hinges on your *other* HW grades, which were irrelevant before this idea
    was introduced
    - No what I said originally is completely fucking correct lmao
    - Extra cred should be treated in a similar way
    - https://www.desmos.com/calculator/xrquhvotdf
    
CSV's should only contain information the program needs to exist after 
termination or that will show up on the report for user 

For each assignment entry into hw.csv, insert_hwopt should generate late_days+1
deadline entries in dl.csv, with blank prindex and c-prindex entries. Then, gaze
should populate these entries by filtering to the relevant df in dl.csv and
computing the local prindexes and c-prindexes for each row based on the
percentage and deadline entries to the left of it. Then it should sum up all
prindexes and input this sum as the prindex for the assignment in hw.csv (same
for c-prindexes)

Filter deadlines for being past datetime.now()

Implement notes!

And then a separate table for hw type info? eg:
Class   | Type     | Total Points | Count | Percentage | Late Policy | Late Phases
CMSC351 | Homework | 100          | 11    | (100/600)/11 
CMSC330 | Projects | Percentage: V | Late Policy: 1.10 
PSYC100 | WS | Percentage: V | Late Policy: S.05
GEOG211 | Lab | Percentage: 100/600 | Late Policy: 3.05

Late Policies table?


(days, cutoff) is all the information needed to specify a "gradual cutoff" policy:
 - (3,5) is 3 late days with -5% deductions each (CMSC330)
 - (1,10) is 1 late day with a -10% deduction (GEOG211)

[(deadline_1, cutoff_1), ... (deadline_n, cutoff_n)]: most generalized late policy?
    - CMSC330 projs is just [(dl, 0.1), (dl+1, 0.9)]
    - PSYC100 WS and SAs are just [(dl, 0.05), (end_of_semester, 0.95)]
    - flexible to future policies
    - this is essentially what will be stored in dl.csv 

GEOG211: 5%24->5%48->5%72
CMSC330: 10%24
INST123: 10%3->20%24->40%48
PSYC100: 5%S

GEOG211: [x+24|5] [x+48|10] [x+72|15]
 - "if you submit it 24 hours late, you get 5% off your original grade. If you
   submit it 48 hours late, you get 10% off your original grade..." And 
   so forth
PSYC100: (end_of_semester_midnight|5)

prev var

type_insert() places late policy notation in a type.csv entry, and hw_insert()
 parses it to generate appropriate hw.csv rows?
    - if the LP-Scheme is written in terms of % deducted from your OG grade, 
    hwopt would have to convert it into the differences either a) in every 
    gaze() call or b) only once because it stores the list of differences in
    some csv (could just store it in type.csv)

lp_insert() asks user for the number of turn-in phases followed by the %
deduction for each LATE phase (which can only exist if # of turn-in phases > 1).
Input goes in the middle of a [0, 1] array and then differences are taken 
(divided by 100) and input into tip(turn-in phases).csv. Then it asks for the
 datetime for each (unique) phase, which is input as a variable (x1, x2, etc.) 
 appended with a "+y", if necessary, where y is the number of hours to jump forward from the
   original deadline. Then, types are inserted with references to lp's (or not).
   When user inserts Assignments of those types, they will be asked to specify 
   x1, x2, etc. and then the lp template will be used with the parametrized
   values to generate the dl rows for the assignment in dl.csv 
    - an assignment type has a late policy (1:1), which has several turn-in
      phases (tips, 1:many)

lp          |phase  |pct |dl
cmsc330proj |1      |0.1 |x1
cmsc330proj |2      |0.9 |x1+1

lp          |phase  |pct    |dl
psyc100wssa |1      |0.05   |x1
psyc100wssa |2      |0.95   |x2

test without writing to csv (instead printing the df), then write to csv?

Don't call datetime.now() over and over again to compute local prindexes, just 
save it as a var and subtract it as needed

short-circuit evaluate cprindex iff commute factor = 0

default commute factor in type.csv?

give hw.type.lp is used by gen() to generate the deadline dataframe that it sums shit 
over. This dataframe is not written to disk!
    - n/a in a type.csv row's lp attribute basically means you turn in what you
      owe on the due date or its gg
    - giving HW an lp attribute only makes sense if you think that a HW's lp can
      differ from that of its type...can this ever be the case?

Are total_tpts, count, and pct both necessary in type.csv?
    - We could just ask for total points iff class.total_pts != n/a and then
      convert it to the appropriate pct and enter just into pct

How to account for varying pcts for assignments that should be the same type?
    - Let type.pct be a default value that you choose to pick in input_hw(). If
      you don't pick it, you enter the pct yourself
    - But actually coming up with a default value in the first place might be
      too much to ask...PSCY100 worksheets case in point
    - what if we make a hw.pct_type attribute? Then lp and pct can be decoupled 
    from type
    - insert_hw() gives you a choice between a template and manual pct input?
    - type.pct can be "man", but type.lp cannot. type.lp can either be an lp
    that's in lp.csv or n/a
    - why not percent templates? cuz different types can have the same lp but
    different types basically never have the same percentages. So we may as well
    couple percentages to the types themselves
    - if class.total_pts != n/a then ask user both for # of the assignment type
    that is scheduled and how much that type is weighed against class.total_pts

let user define x1, x2 in insert_hw()    
"""
