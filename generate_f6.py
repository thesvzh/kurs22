import sys
sys.setrecursionlimit(10000)
from pyeda.inter import exprvar, Variable, point2upoint, expr2truthtable
import itertools

x1, x2, x3, x4, x5, x6, x11, x12, x13, x14, notx11, notx12, notx13, notx14, x21, x22, x23, x24, notx21, notx22, notx23, notx24, x31, x32, x33, x34, notx31, notx32, notx33, notx34, x41, x42, x43, x44, notx41, notx42, notx43, notx44, x51, x52, notx51, notx52, x61, x62, notx61, notx62 = map(
    exprvar, "x1, x2, x3, x4, x5, x6, x11, x12, x13, x14, notx11, notx12, notx13, notx14, x21, x22, x23, x24, notx21, notx22, notx23, notx24, x31, x32, x33, x34, notx31, notx32, notx33, notx34, x41, x42, x43, x44, notx41, notx42, notx43, notx44, x51, x52, notx51, notx52, x61, x62, notx61, notx62".split())
all_vars = [x1, x2, x3, x4, x5, x6, x11, x12, x13, x14, notx11, notx12, notx13, notx14, x21, x22, x23, x24, notx21, notx22, notx23, notx24, x31, x32, x33, x34, notx31, notx32, notx33, notx34, x41, x42, x43, x44, notx41, notx42, notx43, notx44, x51, x52, notx51, notx52, x61, x62, notx61, notx62]

equals = [(x1, [x1, x2, x3, x4, x5, x6]),
          (~x1, [notx11, notx12, notx13, notx14]),
          (x2,[x21, x22, x23, x24]), (~x2,[notx21, notx22, notx23, notx24]),
          (x3, [x31, x32, x33, x34]),
          (~x3, [notx31, notx32, notx33, notx34]),
          (x4, [x41, x42, x43, x44]), (~x4, [notx41, notx42, notx43, notx44]),
          (x5, [x51, x52]), (x6, [x61, x62]), (~x5, [notx51, notx52]), (~x6, [notx61, notx62])]

inputs = [x1, x2, x3, x4, x5, x6]
k6_functions = set()
count = 0
for vec in list(itertools.product(range(3), repeat=40))[::-1]:
    d = dict(zip(all_vars, vec))
    #print("==============================")
    #print(d)
    function = ((x11 & notx21 & notx31 & notx41 & x51 & x61) | (x11 & notx21 & x31 & x41 & x51 & x61) |
                (x11 & notx21 & notx31 & notx41 & notx51 & notx61) | (x11 & notx21 & x31 & x41 & notx51 & notx61) |
                
                (notx11 & x21 & notx31 & notx41 & x51 & x61) | (notx11 & x21 & x31 & x41 & x51 & x61) |
                (notx11 & x21 & notx31 & notx41 & notx51 & notx61) | (notx11 & x21 & x31 & x41 & notx51 & notx61) |
                

                (notx12 & notx22 & x32 & notx42 & x51 & x61) | (notx12 & notx22 & x32 & notx42 & notx51 & notx61) |
                (x12 & x22 & notx32 & x42 & notx51 & notx61) | (x12 & x22 & notx32 & x42 & x51 & x61) |
                
                (notx12 & notx22 & notx32 & x42 & x51 & x61) | (notx12 & notx22 & notx32 & x42 & notx51 & notx61) |
                (x12 & x22 & x32 & notx42 & notx51 & notx61) | (x12 & x22 & x32 & notx42 & x51 & x61) |


                (notx13 & notx23 & notx33 & notx43 & x52 & notx62) | (notx13 & notx23 & notx33 & notx43 & notx52 & x62) |
                (notx13 & notx23 & x33 & x43 & notx52 & x62) | (notx13 & notx23 & x33 & x43 & x52 & notx62) |
                
                (x13 & x23 & notx33 & notx43 & notx52 & x62) | (x13 & x23 & x33 & x43 & x52 & notx62) |
                (x13 & x23 & notx33 & notx43 & x52 & notx62) | (x13 & x23 & x33 & x43 & notx52 & x62) |
                

                (notx14 & x24 & x34 & notx44 & x52 & notx62) | (notx14 & x24 & x34 & notx44 & notx52 & x62) |
                (x14 & notx24 & notx34 & x44 & notx52 & x62) | (x14 & notx24 & notx32 & x44 & x52 & notx62) |
                
                (notx14 & x24 & notx34 & x44 & x52 & notx62) | (notx14 & x24 & notx34 & x44 & notx52 & x62) |
                (x14 & notx24 & x34 & notx44 & notx52 & x62) | (x14 & notx24 & x34 & notx44 & x52 & notx62) )

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

with open("results_6.txt", "w") as f:
    f.write("\n".join(sorted(k4_functions)))

print("# functions: ", len(k4_functions))
