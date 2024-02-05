HF, FH, UE, ES, SP, PU, UB, BJ, JB, BE, EB, BU, PC, CS, SU = ["Home to Route 5", 6], ["Route 5 to Home", 7], ["Shuttle-UM 111 to ESJ", 3], ["ESJ to STEM Library", 3], ["STEM Library to Physics Building", 2], ["Physics Building to Shuttle-UM 111", 3], ["Shuttle-UM 111 to Hornbake", 4], ["Hornbake to HJ Patterson", 3], ["HJ Patterson to Hornbake", 3], ["Hornbake to ESJ", 2], ["ESJ to Hornbake", 2], ["Hornbake to Shuttle-UM 111", 2], ["Physics Building to CS Instructional Center", 4], ["CS Instructional Center to STEM Library", 4], ["STEM Library to Shuttle-UM 111", 3]

inp = input("Which day would you like (M/T/F)? ")
print()

if inp == 'M':
	wl = [HF, UE, ES, SP, PU, FH]
elif inp == 'T':
	wl = [HF, UB, BJ, JB, BE, EB, BU, FH]
else:
	wl = [HF, UE, ES, SP, PC, CS, SU, FH]

sum = 0
for walk in wl:
	print(f"{walk[0]}: {walk[1]}")
	sum += walk[1]
print()
print(f"Total: {sum}")