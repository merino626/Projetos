def ordemc(vetor):
    pos = vetor[0]
    for i in vetor:
        if i >= pos:
            pos = i
        else:
            return False

    return True


vetor = [1, 51, 2, 2, 5, 6, 7, 8]

print(ordemc(vetor))