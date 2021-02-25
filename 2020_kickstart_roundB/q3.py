def decode(ins):
    # print(ins)
    n,s,e,w = 0,0,0,0
    i = 0
    while i < len(ins):
        ch = ins[i]
        if ch == 'N':
            n += 1
        elif ch == 'S':
            s += 1
        elif ch == 'E':
            e += 1
        elif ch == 'W':
            w += 1
        else:
            left_par_i = ins.index('(', i)
            multiplier = int(ins[i:left_par_i])
            j = left_par_i + 1
            open_par = 1
            while j<len(ins):
                if ins[j] == '(':
                    open_par += 1
                if ins[j] == ')':
                    open_par -= 1
                if open_par == 0:
                    break
                j += 1
            right_par_i = j
            # print(ins,i,left_par_i, right_par_i)
            sub_n, sub_s, sub_e, sub_w = decode(ins[left_par_i+1:right_par_i])
            n += sub_n*multiplier
            s += sub_s*multiplier
            e += sub_e*multiplier
            w += sub_w*multiplier
            i = right_par_i
        i += 1
    # print(ins,n,s,e,w)
    return n,s,e,w

def fcn(ins):
    n,s,e,w = decode(ins)
    row = (s-n) % 1000000000 + 1
    col = (e-w) % 1000000000 + 1
    return col, row

t = int(input())
for i in range(1, t + 1):
    instruction = input()
    res = [0, 0]
    res[0], res[1] = fcn(instruction)
    print("Case #{}: {} {}".format(i, res[0], res[1]))
