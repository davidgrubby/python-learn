print('__name__:', __name__)

def add(a, b):
    return a + b

print('test: 2 + 3 =', add(2, 3))


if __name__ == '__main__':
    import sys
    args = sys.argv  
    print(args)
    print(add(int(args[1]), int(args[2])))
