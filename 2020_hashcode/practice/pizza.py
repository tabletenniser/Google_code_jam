def get_opt_solution(max_slices, pizza_slices):
    types_of_pizzas = len(pizza_slices)
    prev_dp_table = [0 for _ in range(max_slices)]
    prev_solution_table = [list() for _ in range(max_slices)]

    for i in range(types_of_pizzas):
        dp_table = [0 for _ in range(max_slices)]
        solution_table = [list() for _ in range(max_slices)]
        print(i)
        for j in range(max_slices):
            if pizza_slices[i] > j:
                dp_table[j] = prev_dp_table[j]
                solution_table[j] = prev_solution_table[j]
            else:
                dp_table_value_select = prev_dp_table[j-pizza_slices[i]] + pizza_slices[i]
                if prev_dp_table[j] > dp_table_value_select:
                    dp_table[j] = prev_dp_table[j]
                    solution_table[j] = prev_solution_table[j]
                else:
                    dp_table[j] = dp_table_value_select
                    solution_table[j] = prev_solution_table[j-pizza_slices[i]] + [i]
        # print(dp_table)
        # print(solution_table)
        prev_dp_table = dp_table
        prev_solution_table = solution_table
    return solution_table[-1]

def get_approx_solution(max_slices, pizza_slices):
    cur_clice_count = 0
    cur_solution = []
    types_of_pizzas = len(pizza_slices)
    for i in range(types_of_pizzas-1, -1, -1):
        p = pizza_slices[i]
        if cur_clice_count + p < max_slices:
            cur_clice_count += p
            cur_solution.append(i)
    cur_solution.sort()
    return cur_solution

max_slices, pizza_types = [int(s) for s in input().split(" ")]
pizza_slices = [int(s) for s in input().split(" ")]
opt_sol=get_opt_solution(max_slices, pizza_slices)
print(len(opt_sol))
print(' '.join(map(str, opt_sol)))
