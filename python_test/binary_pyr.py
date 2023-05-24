from random import randrange

pyr_height = int(input("Enter binary pyramid height: ")) + 1
for i in range(1, pyr_height):
    for j in range(0, i):
        print(randrange(2), end="")  # print input_string with no newline
    print("")  # newline after inner loop concludes
