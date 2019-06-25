
def get_last_one_bouncy(percentage=99):
    initial = 99
    count_bouncy = 0
    while not if_finish(initial, count_bouncy, percentage):
        initial += 1
        list_initial = list(str(initial))
        count_bouncy = bouncy_counter(list_initial, count_bouncy)
    print_f(initial)
    return initial


def bouncy_counter(list_initial, count):
    if is_bouncy(list_initial):
        count += 1
    return count


def non_increasing(l):
    return all(x >= y for x, y in zip(l, l[1:]))


def non_decreasing(l):
    return all(x <= y for x, y in zip(l, l[1:]))


def is_bouncy(l):
    return not (non_increasing(l) or non_decreasing(l))


def if_finish(number, count, percentage):
    if (count*100)/number >= percentage:
        return True

    return False


def print_f(data):
    print(data)


get_last_one_bouncy(50)
