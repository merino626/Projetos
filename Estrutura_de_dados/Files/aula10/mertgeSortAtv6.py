import time
import random


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



def preenchev(v,n):
    for i in range(n):
        v.append(random.randint(0, 100))
n=1000000
print("********************************************************************************")
print("********************************************************************************")
print("teste para ",n)
start_time = time.time()
v1=[]
v2=[]
preenchev(v1,n)
preenchev(v2,n)
elapsed_time=time.time()-start_time
print("tempo preencher vetores",time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))

start_time = time.time()
mergesort(v1,0,len(v1)-1)
elapsed_time=time.time()-start_time
print("tempo mergeSort   ",time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))

start_time = time.time()
v2.sort()
elapsed_time=time.time()-start_time
print("tempo sort Python   ",time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))