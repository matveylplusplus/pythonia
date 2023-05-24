input_string = input("Enter your datum: ")
pyr_height = int(input("Enter pyramid height: ")) + 1

for i in range(1, pyr_height):
    for j in range(0, i):
        print(input_string, end="")  # print input_string with no newline
    print("")  # newline after inner loop concludes
