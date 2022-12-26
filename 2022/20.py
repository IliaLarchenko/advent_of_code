def prepare_data(file="input.txt"):
    with open(file) as file:
        lines = [line.strip() for line in file.readlines()]

    numbers = [int(line) for line in lines]

    data = {"numbers": numbers}

    return data


class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


def list_to_dllist(numbers):
    start = Node(numbers[0])
    end = start
    for n in numbers[1:]:
        node = Node(n)
        node.left = end
        end.right = node
        end = node
    start.left = end
    end.right = start

    return start


def dllist_to_list(start):
    list1 = []
    list1.append(start.value)
    node = start.right
    while node != start:
        list1.append(node.value)
        node = node.right
    return list1


def dllist_to_link_list(start):
    list1 = []
    list1.append(start)
    node = start.right
    while node != start:
        list1.append(node)
        node = node.right
    return list1


def move(node, n, lenght):
    n = n % (lenght - 1)
    if n == 0:
        return

    goal = node
    for _ in range(n):
        goal = goal.right

    old_left = node.left
    old_right = node.right

    new_left = goal
    new_right = goal.right

    old_left.right = old_right
    old_right.left = old_left

    new_left.right = node
    new_right.left = node
    node.right = new_right
    node.left = new_left


def solve1(numbers, **kwargs):
    start = list_to_dllist(numbers)

    for node in dllist_to_link_list(start):
        move(node, node.value, len(numbers))

    node = start
    while node.value != 0:
        node = node.right

    list_0 = dllist_to_list(node)

    return sum([list_0[i % len(list_0)] for i in [1000, 2000, 3000]])


def solve2(numbers, **kwargs):
    start = list_to_dllist([n * 811589153 for n in numbers])

    list_of_links = dllist_to_link_list(start)
    for _ in range(10):
        for node in list_of_links:
            move(node, node.value, len(numbers))

    node = start
    while node.value != 0:
        node = node.right

    list_0 = dllist_to_list(node)

    return sum([list_0[i % len(list_0)] for i in [1000, 2000, 3000]])
