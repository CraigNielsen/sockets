
def generate_messages(n, m):
    arr = []
    for i in range(n, m):
        arr.append("^{}|{}|{}^".format(i, 30,40))
    return arr
