import time


def set_numbers(number, count):
    find_more_number(number, count)


def find_more_number(number, count):
    while not if_finish(number, count):
        number += 1
        list_initial = list(str(number))
        count = bouncy_counter(list_initial, count)
    print_f(number)


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


def if_finish(number, count):
    if (count*100)/number >= 99:
        return True

    return False


def print_f(data):
    print(data)


initial = 99
count_bouncy = 0

start = time.time()
print(set_numbers(initial, count_bouncy), time.time()-start)
