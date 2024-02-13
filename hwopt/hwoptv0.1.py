"""
To do ASAP:
    - insert()
        - insert_class()
        - insert_late_policy()
        - insert_template()
        - insert_assignment()
            - clean_deadlines()
            - place results in temp table, which user can then sort by prindex or c-prindex
    - compute_prindex()

Features for the future, possibly:
    - Being able to go back a page without quitting the whole program with ctrl+c
    - Updating templates updates all users of that template
    - Accounting for drops 
    - Accounting for extra credit
"""

import pandas as pd
from dateutil import parser
import datetime
import numpy
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Union


@dataclass
class Class:
    class_name: str
    major: bool
    total_points: int

    def compute_class_points(self) -> float:
        major_factor = 1 if self.major else 5 / 8
        return major_factor / self.total_points

@dataclass
class LatePolicyTemplate:
    lscheme: list[(float, str)]

    def get_deadline_count(self) -> int:
        return int(((self.scheme[-1])[1].split("|"))[0])


"""@dataclass
class LatePolicy:
    scheme: list[(float, datetime.timedelta)]"""

@dataclass
class PointAssignmentTemplate():
    template_name: str
    points: int

    def compute_template_points(self) -> int:
        return self.points

@dataclass 
class LatePolicyAssignmentTemplate():
    template_name: str
    late_policy_template: LatePolicyTemplate

    def get_late_policy_template(self) -> LatePolicyTemplate:
        return self.late_policy_template

@dataclass
class DualAssignmentTemplate():
    point_assignment_template: PointAssignmentTemplate
    late_policy_assignment_template: LatePolicyAssignmentTemplate

    def compute_template_points(self) -> int:
        return self.point_assignment_template.compute_template_points()
    
    def get_late_policy_template(self) -> LatePolicyTemplate:
        return self.late_policy_assignment_template.get_late_policy_template()



class PointPackage(ABC):
    @abstractmethod
    def compute_points(self) -> float:
        pass
    def push_manual(self, int) -> float:
        pass
    def pull_manual(self, )

@dataclass    
class RawPointPackage(PointPackage):
    points: int

    def compute_points(self) -> float:
        return self.points

@dataclass 
class TemplatedPointPackage(PointPackage):
    assignment_template: AssignmentTemplate

@dataclass
class Assignment:
    assignment_name: str
    school_class: Class
    commute_factor: float
    point_package: PointPackage
    late_policy_package: LatePolicyPackage

"""class assignment(ABC):
    @abstractmethod
    def compute_prindex(self) -> float:"""

############################

class PointTemplate(ABC):
    @abstractmethod
    def compute_assignment_points(self) -> float:
        """Computes the points"""


@dataclass
class EvenDistributionPointTemplate(PointTemplate):
    assignment_count: int
    total_assignment_points: int

    def compute_assignment_points(self) -> float:
        return self.total_assignment_points / self.assignment_count


@dataclass
class SingletonPointTemplate(PointTemplate):
    assignment_points: int

    def compute_assignment_points(self) -> float:
        return self.assignment_points

class AssignmentTemplate(ABC):
    @abstractmethod
    def generate_assignment(self, assignment_name, commute_factor) -> float:
        """Generates an assignment that follows the assignment template."""


@dataclass
class PlpTemplate(AssignmentTemplate):
    template_name: str
    point_template: PointTemplate
    late_policy_package: LatePolicyTemplate

class Assignment(ABC):
    @abstractmethod
    def compute_prindex(self) -> float:
        """Computes da prindex"""


@dataclass
class ManualAssignment(Assignment):
    assignment_name: str
    cclass: Class
    commute_factor: float
    points: int
    late_policy: 

@dataclass
class Assignment:
    assignment_name: str
    cclass: Class
    # points: int
    # point_type: point_type
    # late_policy: lp
    template: AssignmentTemplate
    commute_factor: float

    def compute_prindex(self) -> float:
        return (
            self.cclass.compute_class_points()
            * self.point_template.compute_assignment_points()
        )

    def compute_cprindex(self) -> float:
        return self.commute_factor * self.compute_prindex()


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
    # init
    hwdf = pd.read_csv("hw.csv")
    classdf = pd.read_csv("class.csv")

    for index, row in hwdf.iterrows():
        cfac = row["cfac"]
        using_pct = row["pct"] != "n/a"


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
        - parse l-scheme
            - store array of substrings up to +, ask user for len(set(arr))
              deadlines that go in input_arr,
              impose order on set (if necessary?), create a dict that makes
              set(arr)[0]:, set(arr)[1]:deadline2, etc. Concurrently,
              substrings to the right of + are typecast to ints and stored in a
              3-tuple (p, x, o)
            - if x == set(arr)[0] then compute input_arr[0] 
        - Generates:
            - mpc
            - P_1, ... , P_n, where P_n = P_1 + ... + P_{n-1}
            - dl_1, ... , dl_n
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
    - but remember, we want to compute as much as possible during gen()!!!

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

insert_hw():
    - check hw.type.lp's schematic in tip.csv and ask user for x1, x2, etc.
    - then, write x1, x2, etc. into dl.csv with the appropriate ps on the side
    - all gen() does is filter the appropriate df in dl.csv, compute the sum,
      and enter it into hw.csv as a temporary column. then sorts
    - this would make deadlines and late policy assignments basically immutable
      after entry, unless you write an update() function 
    - we can't write x1, x2, ... into hw.csv because the number of relevant
      deadlines can vary
    - if an assignment's deadline gets extended or something, just input a new
      assignment and/or type with the info adjusted. I don't got time to make
      update() rn

hw count might change, tpts could change (though I've never seen this happen)

where to put # of lectures? class.csv? what if class doesn't have lectures??

maybe I should insist on everything being in pct? this whole thing with tpts and
class points seems to be making the database design very complicated in exchange
for a quick computation that you really only have to do once a semester for each
type (if the type has fixed values). It can also be easily re-computed if
anything changes. Accommodating every possible way a class can present its grade
distributions (in terms of percentages on types, points on types, points on each
member of type, percentages on each member of type) feels like it gives marginal
returns for large investment. This approach also helps performance because of
less if-branching and no point computations
    - "homeworks are collectively worth 100 points and there are 600 total points"
    - "homeworks are collectively worth 1/6th of your grade"
    - "each homework is 10 points and there are 10 homeworks"
    - "each homework is 1/60th of your grade"
    - actually, for psyc100 worksheets I would have to divide the # of points by
      the total amount of points that ws are worth every single fucking time.
      this is kind of annoying but is automating it worth the dev time?
    - Also I would have to use some other calculator (that may use some other
      level of float precision than python does) to get the percent I need, which
      can throw off prindexes. Unless I make a special case for user to input
      fractions, which sounds retarded
    - it feels like unless I make the most robust program imaginable that
      accounts for every possible way grade distributions can be expressed on a
      syllabus you're never going to automate *all* the computation
    - but just because you can't account for every scenario doesn't mean you
      shouldn't account for the most common ones

types are assignment templates meant to automate specified assignment attributes
    - what if we split everything into  p-templates, lp-templates
    - but then we would just want template templates
    - p-templates dont make much sense because very rarely do other classes
      have the same grade distribution
    - lp-templates make sense because late policies often repeat across classes
    - give users the option to not use templates; some assignments are unique
      and just don't repeat
        - get rid of the type attribute on hw; it will be asked for and looked
          up, but all the relevant information will be entered into the hw
          entry. There'll be no need to refer to the type entry
        - but then how would gen() compute the percentages at run-time? It needs
          access to shit like how many points cmsc351 homeworks collectively
          take up...where would that data be placed and how would gen() access
          it? 
        - maybe we should keep the type block but let it be n/a 

what if we just do the ORM? Iterating through each csv already knowing what kind
of object it is seems way easier than iterating through everything at once and
repeatedly checking all the attributes to figure out how to treat it
    - pt_hw.csv + pct_hw.csv. Go through pt_hw knowing *every* entry has a class
      that has a
      total_pts attribute and a template that has total_type_pts and
      type_count. Then go through 
    - I would need 3*2 = 6 hw tables
        - pct man-lp
        - pct type-lp
        - pt man-lp
        - pt type-lp
        - man man-lp
        - man type-lp
    - man is fine. Just split along pt/pct

fuck it. what if we just replaced type.csv with constructors in a hw class

bro holy fucking shit. load every hw assignment in from a db into an array. Then
iterate thru the array and take advantage of polymorphism to call a
compute_prindex() interface method for each one. Then we can just have a list of
tuples (assignment_name, prindex) and then sort the list by prindex

have total type points be a class var for each school class?

class class has an array of assignment_types?

assignment type objects with assignment types (or their fields) being passed
into hw constructor?

man points -> total class points, lp (sc)
man pct -> nothing!
typed points -> total class points, total type points, type count (sc, t)
typed pct -> total type pct, type count (t)

we need 2 db's...one point-wise grade distribution and one pct-wise grade
distribution
    - identical to (inner?) joining class.db and type.db along class_name
    - class_name, major_state, type_name, pct/pts of grade, count, lp
    - total class points can be obtained by summing pt cells (or could be placed
      in class.db) and joined like major_state
    - should be a literal copy-paste from syllabus that you can make in excel or
    sheets and then download
    - every assignment you put in should have a type that's in one of these
    grade distros
    - assignments.db is class_name, type_name, 
x db's
    - ed lp
    - ed nlp
    - ud lp
    - ud nlp
Each assignment type has a distribution function?
    - But if distribution is uneven, the only conceivable reason for having a
      type in the first place 

Classes that deal in percents are just classes where total_points = 100

Assignment templates should just be constructor auto-completers
    - for late policies, yes. But not for point templates: assignments should
      hold references to point templates so that when the point templates change
      the assignment prindex computations change with them

Where should input be asked for??
    - and then he said its polymorphin time and polymorphed all over the place
    - having a form_assignment() method as part of assignment_template's
      interface makes a lot of sense...but how do we avoid redundant code for
      inputting the assignment name and the deadlines and what have you
    - the duplicate fields are name, class, 

We're never gonna have more than 2 different completely unrelated deadlines on a
late policy...right? So why design for an n-ary deadline use case?
    - But what if we do??

1|0
1|24
1|48
1|72

1|0
2|0

make LatePolicyTemplate a class cuz even tho rn it's only going to be
implemented with a single tuple of tuples u might find a better implementation
later and wouldn't have to restructure everything 
    - generate_late_policy() function similar to generate_assignment()?

Late policy templates should never change...if the late policy for your
homeworks changed you should just make a new late policy template and refer your
hws' AssignmentTemplate to the new late policy template
    - this means Assignment needs to have a reference to AssignmentTemplate
      instead of a direct reference to LatePolicyTemplate

could just make a bunch of type factories...

assignment_input()
    - Ask user for class name, name of assignment, commute factor
    - Ask user for template
        - If entered != n/a: 
            - query template in db and figure out what it takes care of
                - if template takes care of points and lp, ask for deadlines
                - if template takes care of only points, ask for late policy and
                  deadlines 
                  if template takes care of only late policy, ask for points and
                  deadlines 
            - enter assignment into db
        - If entered = n/a:
            - ask user for points, Late Policy, deadlines relevant to late
              policy 
            - enter assignment into db

Consider this
    - You have a cmsc351 homework template that accounts for both late policy
      and points, where the late policy is stand
    - you've entered hw9 into the db and are currently working on it
    - an announcement comes out saying that due to the sheer difficulty of the
      assignment, hw9's late policy will change from stand to 1x10
    - what do
        - you don't want to change the template's late policy, because this
          change applies literally only to hw9
        - but how do you change hw9's late policy if its determined strictly via
          reference to the cmsc351hw template 

Modifying a template should modify all assignments that use it, but modifying an
assignment should not modify its template
    - furthermore, you should be able to "un-modify" an assignment back into
      using its template in case you (or the professor) made a mistake (so the
      reference shouldn't just be thrown away) 

All assignments have Points and LatePolicy objects that can be either references
to templates or raw values? With compute_points() and compute_late_policy()
methods 
    - Points
        - Points.manual: bool
        - Points.manpoints: int
        - Points.assignment_template: AssignmentTemplate (optional)
        - Points.compute_points()
            - if manual then return self.manpoints
            - else self.assignment_template.compute_points()
        - Points.set_manual(manpoints)
            - self.manpoints = manpoints
            - manual = on

type.assignment_count / total value of all type.assignments can be computed at
input and entered into AssignmentTemplate just in terms of points   

Interface implementation at the level of Assignment or at the level of
Assignment.PointPackage? 
    - At the level of assignment = field duplication (assignment_name,
      commute_factor, school_class)
    - At the level of PointPackage = PointPackage.compute_points ->
      AssignmentTemplate.compute_points 

type hints in function parameters?

Questions
    - "figure out what it takes care of" is basically a run-time type check that
      can be settled wuth polymorphism by giving the AssignmentTemplate
      interface a generate_assignment() method
    - but then how the fuck do we generate assignments that don't use templates
    - and how the fuck do we implement template overrides

Multiple interfaces?

But why pollute your codebase with interfaces in a world of ducktyping?

How much python do we even really need, anyway?
    - Parsing the late policy needs python
    - Insertion of data needs python
        - user needs to input number of deadlines that varies based on the late
          policy that was selected; this cannot be done in one simple SQL
          statement 
    - I'm going to wager that prindex gen also needs python

Mutable assignment entries would require: 
    - a method that drops all linked dl entries and replaces them with new ones,
      for when a single assignment's lp is modified (re-input of deadlines
      potentially necessary)
    - a method that drops the linked dl entries of every relevant assignment and
      replaces them with new ones (asking the user for re-input on each one!), 
      for when an assignment template's lp is modified 
    - all in the service of an extremely rare edge-case situation that would at
      worst require a re-input of like 2 or 3 assignments? 
    - this functionality cannot be worth the development time

create temp dl table with appended p_n / (deadline minus datetime.now()) column, (SUM GROUPBY assignment_name) * maj_factor * assignment_points * com_fac and then sort desc on inner join of class, assignment tables

late_policy_phase_templates table where deadlines column entries are 1, 1, 2, ... when user indicates they want to use one python fetches the relevant phase set, takes the last entry's number x, asks for x deadlines, maps them w/ 1, 2, 3 ... in a dict, and then loops thru the phase set executing an insert into the late_policy_phases table on each iteration using the dict

when user wants to use a template, the template is fetched as a tuple from templates table and the assignment's insert statement is plugged in w/ the proper elements of the tuple; the assignment holds no reference to the template (as an attribute or otherwise)

insert_class() could just generate a school_class object and then run the object's insert_into_db() method

pass raw input into SchoolClass constructor and then have constructor parse major_state boolean into a self.major_factor field or whatever (or just send it straight into the insert_into_db(), no class required)

generic db_insert()?
    - how to account for varying attribute counts?

don't store major_factor in db...this exposes implementation relevant only to generate_prindex()...just store 1/0 or TRUE/FALSE or M/G
"""
