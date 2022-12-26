def prepare_data(file="input.txt"):
    with open(file) as file:
        lines = [line.strip() for line in file.readlines()]

    grid = [[int(x) for x in lines[i]] for i in range(len(lines))]

    data = {"grid": grid}
    return data


def solve1(grid, **kwargs):
    left = [[-1 for x in grid[i]] for i in range(len(grid))]
    right = [[-1 for x in grid[i]] for i in range(len(grid))]
    up = [[-1 for x in grid[i]] for i in range(len(grid))]
    down = [[-1 for x in grid[i]] for i in range(len(grid))]

    for i in range(len(grid)):
        for j in range(1, len(grid[0])):
            left[i][j] = max(left[i][j - 1], grid[i][j - 1])

    for i in range(len(grid)):
        for j in range(len(grid[0]) - 2, -1, -1):
            right[i][j] = max(right[i][j + 1], grid[i][j + 1])

    for i in range(1, len(grid)):
        for j in range(len(grid[0])):
            up[i][j] = max(up[i - 1][j], grid[i - 1][j])

    for i in range(len(grid) - 2, -1, -1):
        for j in range(len(grid[0])):
            down[i][j] = max(down[i + 1][j], grid[i + 1][j])

    ans = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] > min([left[i][j], right[i][j], up[i][j], down[i][j]]):
                ans += 1

    return ans


def solve2(grid, **kwargs):
    left = [[0 for x in grid[i]] for i in range(len(grid))]
    right = [[0 for x in grid[i]] for i in range(len(grid))]
    up = [[0 for x in grid[i]] for i in range(len(grid))]
    down = [[0 for x in grid[i]] for i in range(len(grid))]

    for i in range(len(grid)):
        for j in range(1, len(grid[0])):
            if grid[i][j] <= grid[i][j - 1]:
                left[i][j] = 1
            else:
                k = j - 1
                while k > 0 and grid[i][j] > grid[i][k]:
                    left[i][j] += left[i][k]
                    k -= left[i][k]
                left[i][j] += 1

    for i in range(len(grid)):
        for j in range(len(grid[0]) - 2, -1, -1):
            if grid[i][j] <= grid[i][j + 1]:
                right[i][j] = 1
            else:
                k = j + 1
                while k < len(grid[0]) - 1 and grid[i][j] > grid[i][k]:
                    right[i][j] += right[i][k]
                    k += right[i][k]
                right[i][j] += 1

    for j in range(len(grid[0])):
        for i in range(1, len(grid)):
            if grid[i][j] <= grid[i - 1][j]:
                up[i][j] = 1
            else:
                k = i - 1
                while k > 0 and grid[i][j] > grid[k][j]:
                    up[i][j] += up[k][j]
                    k -= up[k][j]
                up[i][j] += 1

    for j in range(len(grid[0])):
        for i in range(len(grid) - 2, -1, -1):
            if grid[i][j] <= grid[i + 1][j]:
                down[i][j] = 1
            else:
                k = i + 1
                while k < len(grid) - 1 and grid[i][j] > grid[k][j]:
                    down[i][j] += down[k][j]
                    k += down[k][j]
                down[i][j] += 1

    ans = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if ans < left[i][j] * right[i][j] * up[i][j] * down[i][j]:
                ans = left[i][j] * right[i][j] * up[i][j] * down[i][j]
    return ans
