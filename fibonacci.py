x = int(input("x: "))


def fibonacci(n):
    a = 0
    b = 1
    c = a+b

    if n < 0:
        print("undefiened")

    elif n == 0:
        print(a)

    elif n == 1:
        print(b)

    elif n == 2:
        print(c)

    else:
        for _ in range(n-2):
            a = b
            b = c
            c = a+b

        print(c)


fibonacci(x)
