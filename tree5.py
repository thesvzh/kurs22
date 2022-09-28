import itertools
import sys
import copy

sys.setrecursionlimit(100000)

functions = []
with open('results_5_konf.txt', 'r') as f:
    functions = [tuple([int(x) for x in line.strip()[1:-1].split(',')]) for line in f.readlines()]


def count_new(m, n, k):
    summa = 0
    count0 = 0
    count1 = 0
    if (k == 31):
        print(count0, "-", k, "-", count1)
    else :
        for i in range(m, n):
            a = functions[i][k]
            if a == 0:
                count0 += 1
            else:
                count1 += 1
        k +=1
        if count0 >= count1 :
            
            count_new (m, count0 + m, k)
            #print (m, n, k)
        else:
            
            count_new (m + count0, n, k)
            #print (m, n, k)
    z = [count0, count1]
    if max(z) != 0:
        print(max(z), z.index(max(z)))
    #return z       
    

count_new (0, len(functions) ,0)

