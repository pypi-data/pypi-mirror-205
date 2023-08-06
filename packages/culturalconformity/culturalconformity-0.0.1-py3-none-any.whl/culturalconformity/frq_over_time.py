def frq_over_time():
    D = float(input("Please enter the conformity coefficient: "))
    N = int(input("Please enter the number of generations: "))
    p = float(input("Please enter the starting frequency: "))
    p_over_time = [p]
    for i in range(N):
        new_p = p + D * p * (1 - p) * (2 * p - 1)
        p = new_p
        p_over_time.append(p)
    return p_over_time 


