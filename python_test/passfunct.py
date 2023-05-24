@staticmethod
def _sum(a, b, c=10):
    return a + b + c


@staticmethod
def _passfunct(funct):
    return funct(1, 2)


mystery = _sum
print(_passfunct(mystery))
