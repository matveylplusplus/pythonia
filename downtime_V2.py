from datetime import timedelta


# define TimeBlock class
class TimeBlock:
    def __init__(self, n, t, d):
        self.name = n
        self.time = t
        self.duration = d

    def __str__(self):
        return f"{self.time} ~ {self.name} ({self.duration})"


# main; ask for input from usr
tail = "(y/n)? "
movie = input(f"Are you going to watch movie with mamasha {tail}")
if movie == "y":
    movie_ht = int(input(f"Enter duration (h):"))
    movie_mt = int(input(f"Enter duration (m):"))
    movie_time = timedelta(hours=movie_ht, minutes=movie_mt)
else:
    sanction = input(f"Are you sanctioned {tail}")
    workout = input(f"Are you going to work out {tail}")
    if workout == "y":
        workout_time = timedelta(
            minutes=int(input(f"Enter workout time (round to nearest min): "))
        )
shower = input(f"Are you going to take a shower {tail}")
if shower == "y":
    shave = input(f"Are you going to shave {tail}")

"""
face_clean = input(f"Are you going to clean yo face {tail}")
"""
print("")

# establish symbolic constants
phone_check_time = timedelta(minutes=15)  # subject to change once skool starts

kitchen_final_time = timedelta(minutes=35)
arm_meal_time = timedelta(minutes=30)
vegetable_time = timedelta(minutes=15)
leisure_time = timedelta(hours=1)

base_clean_time = timedelta(minutes=20)
cleanser_time = timedelta(minutes=5)
shower_time = timedelta(minutes=15)
shave_time = timedelta(minutes=30)
buffer_time = timedelta(minutes=10)

top_time = timedelta(hours=9, minutes=35)

# establish composites
sanction_time = arm_meal_time + vegetable_time
non_sanction_time = arm_meal_time + leisure_time

# init list
schedule = []

top_time -= base_clean_time
schedule.append(TimeBlock("Bedprep", top_time, base_clean_time))

top_time -= phone_check_time
schedule.append(TimeBlock("Phone Check", top_time, phone_check_time))

if sanction == "n":
    top_time -= non_sanction_time
    schedule.append(
        TimeBlock("Final Meal & Leisure", top_time, non_sanction_time)
    )

    top_time -= kitchen_final_time
    schedule.append(
        TimeBlock("Final + Breakfast Meal Prep", top_time, kitchen_final_time)
    )

top_time -= cleanser_time
schedule.append(TimeBlock("Apply Cleanser", top_time, cleanser_time))

if shower == "y":
    if shave == "y":
        top_time -= shave_time
        schedule.append(TimeBlock("Shave", top_time, shave_time))
    top_time -= shower_time
    schedule.append(TimeBlock("Shower", top_time, shower_time))

if movie == "n" and workout == "y":
    top_time -= workout_time
    schedule.append(TimeBlock("Workout", top_time, workout_time))
elif movie == "y":
    top_time -= movie_time
    schedule.append(TimeBlock("Movie", top_time, movie_time))

    top_time -= kitchen_final_time
    schedule.append(
        TimeBlock("Final + Breakfast Meal Prep", top_time, kitchen_final_time)
    )

schedule.reverse()
print(*schedule, sep="\n")
print("")
