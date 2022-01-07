def mergesort(lst,ini,fim):
    if (fim<=ini): #base da recursão
        return
    meio=(ini+fim)//2
    mergesort(lst,ini,meio)
    mergesort(lst,meio+1,fim)
    intercala(lst,ini,meio,fim)


def intercala(lst,ini,meio,fim):
   aux=[]
   esq=ini
   dir=meio+1
   while (esq<=meio and dir <=fim):
        if (lst[esq]<=lst[dir]):
           aux.append(lst[esq])
           esq+=1
        else:
            aux.append(lst[dir])
            dir+=1
   while (esq<=meio):
       aux.append(lst[esq])
       esq+=1
   while (dir<=fim):
       aux.append(lst[dir])
       dir+=1
   lst[ini:fim+1]=aux
   return lst

# v=[7,8,3,5,4]
# mergesort (v,0,len(v)-1)
# print(v)

print(intercala([1,2,3,4,5, 6], 0, 2, 5))