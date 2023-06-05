from collections import deque


def dfs_free(matrix, visited, i, j, parking_slots, parking_busy, airports_main, exception):
    rows = len(matrix)
    cols = len(matrix[0])
    visited[i][j] = True

    if (i, j) in parking_slots and (i,j) not in exception:
        parking_busy.append((i, j))
        return i, j

    result = None
    for x, y in [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]:
        if 0 <= x < rows and 0 <= y < cols and matrix[x][y] and not visited[x][y]:
            res = dfs_free(matrix, visited, x, y, parking_slots, parking_busy, airports_main, exception)
            if res is not None:
                result = res
                break

    return result


def inside(matrix_bool, parking_main, parking_busy, parking_aux, event, events_main, airports_main, exception, saved_path):
    visited = [[False for element in range(len(matrix_bool[0]))] for element in range(len(matrix_bool))]

    event_index = events_main.index(event)


    for i in range(len(matrix_bool)):
        for j in range(len(matrix_bool[0])):
            if (i, j) in airports_main:
                busy = dfs_free(matrix_bool, visited, i, j, parking_main, parking_busy, airports_main, exception)
                i = 1
                while busy is None and event_index > 0:
                    event = events_main[event_index - i]
                    help_back = parking_aux.popleft()
                    visited = [[False for element in range(len(matrix_bool[0]))] for element in range(len(matrix_bool))]
                    matrix_bool[help_back[1][0]][help_back[1][1]] = True
                    parking_main.append(help_back[1])
                    exception.appendleft(help_back[1])
                    parking_busy.remove(help_back[1])
                    saved_path.pop()
                    busy = dfs_free(matrix_bool, visited, i, j, parking_main, parking_busy, airports_main, exception)
                    i += 1

                if busy is not None:
                    if len(exception) > 0:
                        exception.clear()
                    parking_aux.appendleft((event, busy))
                    saved_path.append(busy)
                    matrix_bool[busy[0]][busy[1]] = False
                    parking_main.remove(busy)
                    return parking_aux, saved_path, event, exception
                else:
                    return None


def dfs_busy(matrix, visited, i, j, parking_main, parking_busy, parking_slot, airports_main):
    rows = len(matrix)
    cols = len(matrix[0])
    visited[i][j] = True

    if (i, j) in airports_main:
        parking_busy.remove(parking_slot)
        return parking_slot

    result = None
    for x, y in [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]:
        if 0 <= x < rows and 0 <= y < cols and matrix[x][y] and not visited[x][y]:
            res = dfs_busy(matrix, visited, x, y, parking_main, parking_busy, parking_slot, airports_main)
            if res is not None:
                result = res
                break
    return result


def out(matrix_bool, parking_main, parking_busy, parking_aux, event, airports_main):
    visited = [[False for element in range(len(matrix_bool[0]))] for element in range(len(matrix_bool))]
    event *= -1
    parking_slot = 0

    for item in parking_aux:
        if item[0] == event:
            parking_slot = item[1]
            break

    for i in range(len(matrix_bool)):
        for j in range(len(matrix_bool[0])):
            if matrix_bool[i][j] == False and (i, j) == parking_slot:
                busy = dfs_busy(matrix_bool, visited, i, j, parking_main, parking_busy, parking_slot, airports_main)
                if busy is not None:
                    parking_aux.remove((event, busy))
                    matrix_bool[busy[0]][busy[1]] = True
                    parking_main.append(busy)
                    event *= -1
                    return parking_aux
            else:
                continue


def pathway(matrix_main, matrix_free, matrix_bool, parking_main, airports_main, events_main):
    parking_aux = deque()
    parking_busy = deque()
    saved_path = deque()
    exception = deque()

    index = 0
    while index < len(events_main):
        event = events_main[index]
        if event > 0:
            obteined_data = inside(matrix_bool, parking_main, parking_busy, parking_aux, event, events_main,
                                   airports_main, exception, saved_path)
            if obteined_data is None:
                saved_path = None
            else:
                """if obteined_data[1] in saved_path:
                    saved_path.remove(obteined_data[1])"""
                saved_pat = obteined_data[1]
                event = obteined_data[2]


        else:
            verify = out(matrix_bool, parking_main, parking_busy, parking_aux, event, airports_main)
            if verify is not None:
                parking_aux = verify
            else:
                return None

        index = events_main.index(event) + 1

    return saved_path


def main():
    events_order = 1
    while events_order < 22:

        inputs = input().split()
        planes = int(inputs[0])

        if planes != 0:
            row = int(inputs[1])

            matrix_main = [[
                "Free" if element == '..' else "Airport" if element == '==' else "Busy" if element == '##' else int(
                    element) for element in input().split()] for i in range(row)]

            parking_main = []
            for rows in range(len(matrix_main)):
                for columns in range(len(matrix_main[rows])):
                    if isinstance(matrix_main[rows][columns], int):
                        parking_main.append((rows, columns))

            airports_main = []
            for rows in range(len(matrix_main)):
                for columns in range(len(matrix_main[rows])):
                    if matrix_main[rows][columns] == "Airport":
                        airports_main.append((rows, columns))

            matrix_free = [[
                "Free" if element == 'Free' else "Airport" if element == 'Airport' else "Busy" if element == 'Busy' else "Free"
                for element in matrix_main[rows]] for rows in range(row)]

            matrix_bool = [[False if element == 'Busy' else True for element in matrix_free[rows]] for rows in
                           range(row)]

            if len(parking_main) == 0:
                saved_path = None
            else:
                events_main = [int(x) for x in input().split()]
                saved_path = pathway(matrix_main, matrix_free, matrix_bool, parking_main, airports_main, events_main)
        else:
            saved_path = None

        if saved_path is not None:
            saved_path_fixed = []
            for element in saved_path:
                fila = element[0]
                columna = element[1]

                if matrix_main[fila][columna] > 0:
                    saved_path_fixed.append(matrix_main[fila][columna])

            formatted = " ".join([f"{num:02}" for num in saved_path_fixed])
            print("Case", events_order, ":", "Yes")
            print(formatted + "\n")
        else:
            print("Case", events_order, ":", "No" + "\n")

        events_order += 1


if __name__ == '__main__':
    main()
