def rounding(frqs):
    """
    The input to this function is frqs, a list of frequencies that all must
    be between 0 and 1 and sum to 1. The output is the list of frequencies
    without rounding error.
    """
    frqs_in_bounds = []
    for frq in frqs:  # Ensure that all frequencies are in [0,1]
        if frq < 0:
            frq = 0
        elif frq > 1:
            frq = 1
        frqs_in_bounds.append(frq)
    normalizer = sum(frqs_in_bounds)
    return [frq / normalizer for frq in frqs_in_bounds]

def factorial(num):
    result = 1
    for i in range(2, num+1):
        result *= i
    return result

def get_states(n, m):
    """
    This function takes in n, the number of role models, and m, the number
    of phenotypes, and outputs all possible role model states.
    Credit to: Mark Tolonen, 2019, “Generate all possible lists of length N that sum to S in Python.”
    https://stackoverflow.com/questions/7748442/generate-all-possible-lists-of-length-n-that-sum-to-s-in-python
    """
    if m == 1:
        yield (n,)
    else:
        for elem in range(n + 1):
            for state in get_states(n - elem, m - 1):
                yield (elem,) + state

def p_next_gen(p, n, **coeff_dict):
    pr = 9  # Precision
    p = rounding(p)
    m = len(p)

    p_next_gen = [None] * m
    for j in range(m):
        p_next_gen[j] = p[j]  # This is the first term in Eq. 4 of Denton et al. 2022

    states = list(get_states(n, m))  # Get all possible role model states
    for x in states:  # For each role model state

        # Find the unique string for each symmetrical role model configuration and get d
        x_copy = list(x).copy()
        x_copy.sort()
        x_str = str(x_copy[0])
        for a in range(1, len(x_copy)):
            x_str = x_str + str(x_copy[a])
        d = coeff_dict[x_str]

        # Find numerator and denominator, which is the same for all elements of p_next_gen given x
        numerator = factorial(n)
        denominator = 1
        for l in range(len(x)):
            numerator *= p[l] ** (x[l])
            denominator *= factorial(x[l])

        # Find denom_high and denom_low
        x_subset = [j for j in x if j != 0]
        x_subset.sort(reverse=True)
        x_avg = n / len(x_subset)

        index = 0
        denom_high = 0
        if x_subset[index] > round(x_avg, pr):
            while x_subset[index] > round(x_avg, pr):
                denom_high += x_subset[index]
                index += 1
        else:  # All elements are equal, and they equal the average
            denom_high = 0

        index = len(x_subset) - 1
        denom_low = 0
        if x_subset[index] < round(x_avg, pr):
            while x_subset[index] < round(x_avg, pr):
                denom_low += 1 / (x_subset[index])
                index -= 1
        else:  # All elements are equal, and they equal the average
            denom_low = 0

            # Finally, find g_i(x)*d(x) for each element
        for l in range(m):
            x_l = x[l]
            if (round(d, pr) != 0 and round(x_l, pr) != 0 and round(x_l, pr) != n
                    and (round(x_l, pr) != round(x_avg, pr))):
                if x_l > x_avg:
                    conform = (x_l / denom_high) * (d / n)
                    p_next_gen[l] += float((conform * numerator / denominator))
                elif x_l < x_avg:
                    conform = - (1 / x_l) * (1 / denom_low) * (d / n)
                    p_next_gen[l] += float((conform * numerator / denominator))

    return rounding(p_next_gen)


def frq_over_time(generations, initial_p_vec, n, **coeff_dict):
    p = rounding(initial_p_vec)
    m = len(p)

    all_p_over_time = [[None]] * m
    for j in range(m):
        all_p_over_time[j] = [p[j]]

    for i in range(generations):
        p = p_next_gen(p, n, **coeff_dict)
        for j in range(m):
            all_p_over_time[j].append(p[j])

    return all_p_over_time