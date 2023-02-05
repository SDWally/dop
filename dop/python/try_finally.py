# try return except finally 的测试

def a():
    sum = 0
    try:
        # c = 10 / 0
        sum += 10
        return 100
    except:
        sum += 20
    finally:
        sum += 30
        print("2")
        return sum

print(a())



