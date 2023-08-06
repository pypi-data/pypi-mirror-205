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

def choose_n():
    msg = "Number of role models n = "
    n = float(input(msg))
    while not n.is_integer() or n < 3:
        n = float(input("That is not valid; n must be an integer bigger than 2. " + msg))

    ack = '0'
    if n > 50:
        msg = "This n is large, and the code might be slow. \nEnter 0 to change n or any other key to proceed."
        ack = input(msg)
        if ack == '0':
            n = choose_n()
        else:
            return int(n)
    return int(n)

def choose_m():
    msg = "How many cultural variants do you have? m = "
    m = float(input(msg))
    while not m.is_integer() or m < 2:
        m = float(input("That is not valid; m must be an integer bigger than 1. " + msg))

    ack = '0'
    if m > 50:
        msg = "This m is large, and the code might be slow.\nEnter 0 to change m or any other key to proceed."
        ack = input(msg)
        if ack == '0':
            m = choose_m()
        else:
            return int(m)
    return int(m)

def choose_d(d_min, d_max, denom_high, denom_low, x_vec, n):
    pr = 9  # Precision for rounding
    # Redo this because need it again
    x_subset = [j for j in x_vec if j != 0]
    x_avg = n / len(x_subset)

    msg = "For x = " + str(x_vec) + ", choose d(x) \nbetween " + str(d_min) + " and " + str(d_max) + ". \n(For help, enter '?')"

    d = input(msg)
    if d == '?':
        # Find g_i(x)*d(x) for each element
        g_values = []
        for l in range(len(x_vec)):
            x_l = x_vec[l]
            if (round(x_l, pr) == 0) or (round(x_l, pr) == n) or (round(x_l, pr) == round(x_avg, pr)):
                g_values.append(0)
            elif x_l > x_avg:
                g_values.append(x_l / denom_high)
            elif x_l < x_avg:
                g_values.append(- (1 / x_l) * (1 / denom_low))

        g_msg = ("For a given xi in x = " + str(x_vec) + ", the value of d(x) that you choose \n"
                 + "will be divided by the number of role models, " + str(n) + ", and multiplied \n"
                 + "by gi where g = " + str(g_values) + ". Remember that this d(x) must be \n"
                 + "between " + str(d_min) + " and " + str(d_max) + ". Please enter your choice: ")
        d = input(g_msg)

    d = float(d)
    while d > d_max or d < d_min:
        d = input("This d(x) is invalid or out of bounds; try again.")
        d = choose_d(d_min, d_max, denom_high, denom_low, x_vec, n)

    return float(d)

def choose_conform_coeffs(n, m):
    pr = 9  # Precision used for rounding
    states = list(get_states(n, m))  # Get all possible role model states
    previous_states = {}  # This dictionary will store previous, symmetrical role model states

    for x_vec in states:  # For each role model state
        # Make a unique string for each symmetrical role model configuration (to be used later)
        x_vec_copy = list(x_vec).copy()
        x_vec_copy.sort()
        x_str = str(x_vec_copy[0])
        for a in range(1, len(x_vec_copy)):
            x_str = x_str + str(x_vec_copy[a])

            # Find the bounds on d(x)
        x_subset = [j for j in x_vec if j != 0]
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

        if x_str not in previous_states:
            if round(denom_high, pr) == 0 or round(denom_low, pr) == 0:
                d = 0
            else:
                d_min = -1 * denom_high
                d_max = ((n / x_subset[0]) - 1) * denom_high

                d_min = round(d_min, pr)
                d_max = round(d_max, pr)
                d = choose_d(d_min, d_max, denom_high, denom_low, x_vec, n)

            previous_states[x_str] = float(d)

    return previous_states

def choose_p_vec(m):
    p_vec = []
    for i in range(1, m):
        msg = " frequency of cultural variant " + str(i)
        pi = float(input("Enter the" + msg))
        while sum(p_vec) + pi > 1:
            pi = float(input("The sum of all frequencies cannot exceed 1. \nChoose a different" + msg))
        p_vec.append(pi)

    last_pi = 1 - sum(p_vec)
    p_vec.append(last_pi)

    return p_vec

def interactive():
    intro = input("Press ? for a detailed description of this function or any key to continue.")
    if intro == '?':
        print("This function will allow you to specify conformity coefficients, initial variant frequencies, \n"
              + "and more, but only one option at a time. Make sure to store your results in a variable, e.g., \n"
              + "do not write interactive() all by itself but rather, say, x = interactive() so that \n"
              + "your results will go into the variable called x. They will be in the appropriate format \n"
              + "for input into future functions. See github.com/kaleda/culturalconformity for how to use \n"
              + "the output of the interactive() function in the other functions. Let's get started!")

    msg = "Enter 1 to make your dictionary of conformity coefficients. \nEnter 2 to make your list of initial frequencies. \nEnter 9 to quit. "
    answer = float(input("What would you like to do? \n" + msg))
    while not answer.is_integer() or answer < 1 or answer > 9:
        answer = float(input("Sorry, that was not a valid number. \n" + msg))

    if answer == 1 or answer == 2:
        m = choose_m()
    if answer == 1:  # Make your dictionary of conformity coefficients
        n = choose_n()
        coeff_dict = choose_conform_coeffs(n, m)
        return coeff_dict
    if answer == 2:
        p_vec = choose_p_vec(m)
        return p_vec


