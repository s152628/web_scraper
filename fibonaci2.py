def fibonaci(n, diepte):
    indent = 6 * diepte * " "
    print("{}fibonaci({})".format(indent, n))
    if n <= 2:
        print("{}return {}".format(indent, 1))
        return 1
    value = fibonaci(n - 1, diepte + 1) + fibonaci(n - 2, diepte + 1)
    print("{}return {}".format(indent, value))
    return value


print(fibonaci(5, 0))
