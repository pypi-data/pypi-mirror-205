def rounding(frqs):
    """
    The input to this function is frqs, a list of frequencies that all must
    be between 0 and 1 and sum to 1. The output is the list of frequencies
    without rounding error.
    """
    frqs_in_bounds = []
    for frq in frqs:  # Ensure that all frequencies are in [0,1]
        if frq < 0: frq = 0
        elif frq > 1: frq = 1
        frqs_in_bounds.append(frq)
    normalizer = sum(frqs_in_bounds)
    return [frq / normalizer for frq in frqs_in_bounds]


def frq_over_time():
    D = float(input("Please enter the conformity coefficient: "))
    N = int(input("Please enter the number of generations: "))
    p = float(input("Please enter the starting frequency: "))
    p_over_time = [p]
    for i in range(N):
        all_frqs = [p, 1-p] # Just testing if a function works
        all_frqs = rounding(all_frqs)
        p = all_frqs[0]
        new_p = p + D * p * (1 - p) * (2 * p - 1)
        p = new_p
        p_over_time.append(p)
    return p_over_time


