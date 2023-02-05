def a():
    sum = 0
    try:
        c = 10 / 0
        sum += 10
        return sum
    except:
        sum += 20
    finally:
        sum += 30
        return sum

print(a())



