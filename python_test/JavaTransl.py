print("\n\n\nTHIS IS PYTHON\n\n\n")
data = {"Texas": "Smash", "Vegas": "Smash"}  # hashmap/"dictionary"

for key, val in data.items():
    print(key + "=" + val)
print(len(data))

x = [1, 2, 4, 5, 3, 3, 21, 2, 21, 2, 313, 1, 23, 142, 4]


def func(i):
    return i % 2 == 0


mp = filter(func, x)
print(list(mp))
