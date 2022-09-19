
from pyeda.inter import exprvar, Variable, point2upoint, expr2truthtable
import itertools

x1, x2, x3, x4, x5, x11, x12, x13, x14, notx11, notx12, notx13, notx14, x21, x22, notx21, notx22, x31, x32, notx31, notx32, x41, x42, notx41, notx42, x51, x52, notx51, notx52 = map(
    exprvar, "x1, x2, x3, x4, x5, x11, x12, x13, x14, notx11, notx12, notx13, notx14, x21, x22, notx21, notx22, x31, x32, notx31, notx32, x41, x42, notx41, notx42, x51, x52, notx51, notx52".split())
all_vars = [x11, x12, x13, x14, notx11, notx12, notx13, notx14, x21, x22, notx21, notx22, x31, x32, notx31, notx32, x41, x42, notx41, notx42, x51, x52, notx51, notx52, x1, x2, x3, x4, x5]

equals = [(x1, [x11, x12, x13, x14]), (~x1, [notx11, notx12, notx13, notx14]),
          (x2, [x21, x22]), (~x2, [notx21, notx22]),
          (x3, [x31, x32]), (~x3, [notx31, notx32]),
          (x4, [x41, x42]), (~x4, [notx41, notx42]),
          (x5, [x51, x52]), (~x5, [notx51, notx52])]

inputs = [x1, x2, x3, x4, x5]
k5_functions = set()
count = 0
for vec in list(itertools.product(range(3), repeat=24))[::-1]:
    d = dict(zip(all_vars, vec))
    #print("==============================")
    #print(d)
    function = ((x11 & x21 & notx12 & x41 & x51) | (x11 & x21 & notx12 & notx41 & notx51) | 
                (x11 & x21 & x31 & x12 & x41 & x51) | (x11 & x21 & x31 & x12 & notx41 & notx51) |
                (x11 & notx31 & notx21 & x12 & x41 & x51)| (x11 & notx31 & notx21 & x12 & notx41 & notx51) |
                (x11 & notx31 & notx21 & x31 & notx12 & x41 & x51) | (x11 & notx31 & notx21 & x31 & notx12 & notx41 & notx51)|
                (notx11 & notx21 & x12 & x41 & x51)|(notx11 & notx21 & x12 & notx41 & notx51)|
                (notx11 & notx21 & notx31 & notx12 & x41 & x51)|(notx11 & notx21 & notx31 & notx12 & notx41 & notx51)|
                (notx11 & notx31 & x21 & notx12 & x41 & x51)|(notx11 & notx31 & x21 & notx12 & notx41 & notx51)|
                (notx11 & notx31 & x21 & x31 & x12 & x41 & x51)|(notx11 & notx31 & x21 & x31 & x12 & notx41 & notx51)|

                (x13 & x22 & notx14 & x42 & notx52) | (x13 & x22 & notx14 & notx42 & x52) |
                (x13 & x22 & notx32 & x14 & x42 & notx52) | (x13 & x22 & notx32 & x14 & notx42 & x52) |
                (x13 & x32 & notx22 & x14 & x42 & notx52) | (x13 & x32 & notx22 & x14 & notx42 & x52) |
                (x13 & x32 & notx22 & notx32 & notx14 & x42 & notx52) | (x13 & x32 & notx22 & notx32 & notx14 & notx42 & x52) |
                (notx13 & notx22 & x14 & x42 & notx52) | (notx13 & notx22 & x14 & notx42 & x52) |
                (notx13 & notx22 & x32 & notx14 & x42 & notx52) | (notx13 & notx22 & x32 & notx14 & notx42 & x52) |
                (notx13 & x32 & x22 & notx14 & x42 & notx52) | (notx13 & x32 & x22 & notx14 & notx42 & x52) |
                (notx13 & x32 & x22 & notx32 & x14 & x42 & notx52) | (notx13 & x32 & x22 & notx32 & x14 & notx42 & x52)

                )
    
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
    k5_functions.add(str(tuple(map(lambda x: x-1, list(expr2truthtable(function).pcdata)))))
    count += 1
    #print(count)
    #if count > 1000:
        #break

with open("results_5_konf.txt", "w") as f:
    f.write("\n".join(sorted(k5_functions)))

print("# functions: ", len(k5_functions))
