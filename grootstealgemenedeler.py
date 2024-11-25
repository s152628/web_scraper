def grootstedeler(a, b):
    if a % b == 0:
        return b
    return grootstedeler(b, a % b)


print(grootstedeler(21, 14))
