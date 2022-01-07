v = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

k = len(v) - 1
s = 0
while k >= 0:
    print(k)
    s += v[k]
    k -= 1

print(s)