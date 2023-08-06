def find_factorial(n):

    if not n:
        return 1
    return find_factorial(n - 1) * n