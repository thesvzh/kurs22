import sys
sys.setrecursionlimit(10000)
from pyeda.inter import exprvar, Variable, point2upoint, expr2truthtable
import itertools

x1, x2, x3, x4, x11, x12, notx11, notx12, x21, x22, notx21, notx22, x31, x32, notx31, notx32, x41, x42, notx41, notx42 = map(
    exprvar, "x1, x2, x3, x4, x11, x12, notx11, notx12, x21, x22, notx21, notx22, x31, x32, notx31, notx32, x41, x42, notx41, notx42".split())
all_vars = [x11, x12, notx11, notx12, x21, x22, notx21, notx22, x31, x32, notx31, notx32, x41, x42, notx41, notx42]

equals = [(x1, [x11, x12]), (~x1, [notx11, notx12]), (x2,[x21, x22]), (~x2,[notx21, notx22]), (x3, [x31, x32]),
          (~x3, [notx31, notx32]), (~x4, [notx41, notx42]), (x4, [x41, x42])]

inputs = [x1, x2, x3, x4]
k4_functions = set()
count = 0
for vec in list(itertools.product(range(3), repeat=16))[::-1]:
    d = dict(zip(all_vars, vec))
    #print("==============================")
    print(d)
    function = ((x11 & notx21 & notx31 & notx41) | (x11 & notx21 & x31 & x41) |
                (notx11 & x21 & notx31 & notx41) | (notx11 & x21 & x32 & x41) |
                (notx12 & notx22 & x32 & notx42) | (notx12 & notx22 & notx32 & x42) |
                (x12 & x22 & x32 & notx42) | (x12 & x22 & notx32 & x42) )
    restrict_dict = {key:value for key, value in d.items() if value in (0, 1)}
    #print(restrict_dict)
    function = function.restrict(restrict_dict)
    #print(function)
    for var, vars_lst in equals:
        for v in vars_lst:
            function = function.compose({v: var})
    #print(function)
    fictitious_vars = [v for v in inputs if v not in function.inputs]
    for v in fictitious_vars:
        function = function & (v | ~v)
    #print(function)
    #print(expr2truthtable(function))
    k4_functions.add(str(tuple(map(lambda x: x-1, list(expr2truthtable(function).pcdata)))))
    count += 1
    #print(count)
    #if count > 1000:
        #break

with open("results.txt", "w") as f:
    f.write("\n".join(sorted(k4_functions)))

print("# functions: ", len(k4_functions))
