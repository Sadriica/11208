from collections import deque

def backtracking(matrix,visited,i,j, parking_slots,parking_aux, parking_busy,airports_main, event, events_main, obteined_data, exception):
    event_index = events_main.index(event) - 1
    event = events_main[event_index]
    parking_aux.remove((event, obteined_data))
    matrix[obteined_data[0]][obteined_data[1]] = True
    parking_slots.append(obteined_data)
    exception.append(obteined_data)
    return dfs_free(matrix, visited, i, j, parking_slots,parking_aux, parking_busy, airports_main, event, obteined_data, exception)


def dfs_free(matrix, visited, i, j, parking_slots,parking_aux, parking_busy, airports_main, event, events_main, obteined_data, exception):
    visited[i][j] = True
    event_index = events_main.index(event)

    if (i, j) in parking_slots and (i,j) not in exception:
        parking_busy.append((i, j))
        return i, j

    result = None

    if result is None and event:
        backtracking(matrix,visited,i,j, parking_slots,parking_aux, parking_busy,airports_main,event,events_main, obteined_data, exception)
        return result

    for x, y in [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]:
        if 0 <= x < len(matrix) and 0 <= y < len(matrix[0]) and matrix[x][y] and not visited[x][y]:
            res = dfs_free(matrix, visited, x, y, parking_slots,parking_aux, parking_busy, airports_main, event, events_main, obteined_data, exception)
            if res:
                result = res  # Si el resultado de la llamada recursiva no es None, establecemos result en ese valor
                break

        return result


def inside(matrix_bool, parking_main, parking_busy, parking_aux, airports_main, event, events_main, obteined_data):
    visited = [[False for element in range(len(matrix_bool[0]))] for element in range(len(matrix_bool))]

    exception = []
    for i in range(len(matrix_bool)):
        for j in range(len(matrix_bool[0])):
            if (i, j) in airports_main:
                busy = dfs_free(matrix_bool, visited, i, j, parking_main,parking_aux, parking_busy, airports_main, event,events_main, obteined_data, exception)
                if busy is not None:
                    parking_aux.appendleft((event, busy))
                    saved_path = busy
                    matrix_bool[busy[0]][busy[1]] = False
                    parking_main.remove(busy)
                    print("Este es el evento: ", event)
                    print("Busy: ", busy)
                    print("Este es Parking_aux: ", parking_aux)
                    print("Este es parking_main: ", parking_main)
                    print("------------")
                    return parking_aux, saved_path
                else:
                    return None


def dfs_busy(matrix, visited, i, j, parking_main, parking_busy, parking_slot, airports_main):
    visited[i][j] = True

    if (i, j) in airports_main:
        parking_busy.remove(parking_slot)
        return parking_slot

    result = None  # Inicializamos la variable result en None
    for x, y in [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]:
        if 0 <= x < len(matrix) and 0 <= y < len(matrix[0]) and matrix[x][y] and not visited[x][y]:
            res = dfs_busy(matrix, visited, x, y, parking_main, parking_busy, parking_slot, airports_main)
            if res:
                result = res  # Si el resultado de la llamada recursiva no es None, establecemos result en ese valor
                break

    return result


def out(matrix_bool, parking_main, parking_busy, parking_aux, event, airports_main):
    visited = [[False for element in range(len(matrix_bool[0]))] for element in range(len(matrix_bool))]
    event *= -1
    print(event)
    parking_slot = 0

    for item in parking_aux:
        if item[0] == event:
            parking_slot = item[1]
            break

    for i in range(len(matrix_bool)):
        for j in range(len(matrix_bool[0])):

            ##Para esta casilla se debe empezzar en el parking_slot donde esta ubicado el evento
            if matrix_bool[i][j] == False and (i, j) == parking_slot:
                busy = dfs_busy(matrix_bool, visited, i, j, parking_main, parking_busy, parking_slot, airports_main)
                if busy is not None:
                    parking_aux.remove((event, busy))
                    matrix_bool[busy[0]][busy[1]] = True
                    parking_main.append(busy)
                    event *= -1
                    print("Este es el evento: ", event)
                    print("Busy: ", busy)
                    print("Este es Parking_aux: ", parking_aux)
                    print("Este es parking_main: ", parking_main)
                    print("------------")
                    return parking_aux
            else:
                continue

                ##Tengo que verficar que validacion se hace para esta casilla


def pathway(matrix_main, matrix_free, matrix_bool, parking_main, airports_main, events_main):
    parking_aux = deque()
    parking_busy = deque()
    saved_path = deque()
    obteined_data = 0,0

    for event in events_main:

        event_index = events_main.index(event)
        if event > 0:
            print("Este es un evento de Entrada")
            ##Me falta añadir todos los parqueaderos que uso y hacer la validacion de YES o NO
            obteined_data = inside(matrix_bool, parking_main, parking_busy, parking_aux,airports_main, event, events_main, obteined_data[1])
            print(obteined_data)
            if obteined_data is None:
                saved_path = None
            else:
                saved_path.append(obteined_data[1])
                print("EL CAMINO GUARDADO ES: ", saved_path)


        else:
            print("Este es un evento de Salida")
            out(matrix_bool, parking_main, parking_busy, parking_aux, event, airports_main)

    return saved_path


def print_main(matrix_main, matrix_free, matrix_bool, parking_main, aiports_main, events_main):
    print("----------------------------")
    print("Matrix: ")
    print(matrix_main)
    print("----------------------------")
    print("Matrix Free: ")
    print(matrix_free)
    print("----------------------------")
    print("Matrix Bool: ")
    print(matrix_bool)
    print("----------------------------")
    print("Parking Slots: ")
    print(parking_main)
    print("----------------------------")
    print("Airports: ")
    print(aiports_main)
    print("----------------------------")
    print("Events List: ")
    print(events_main)
    print("----------------------------")
    print("DONE")
    print("----------------------------")
    print('')


def main():
    cant_event = 1
    while cant_event < 22:

        ##print("ESTE ES EL EVENTO: ", cant_event)

        inputs = input().split()
        planes = int(inputs[0])

        if planes != 0:
            row = int(inputs[1])
            column = int(inputs[2])

            matrix_main = [[
                "Free" if element == '..' else "Airport" if element == '==' else "Busy" if element == '##' else int(
                    element) for element in input().split()] for i in range(row)]

            # Llenar el parqueadero con el parqueadero y su posicion en matrix_main
            parking_main = []
            for rows in range(len(matrix_main)):
                for columns in range(len(matrix_main[rows])):
                    if isinstance(matrix_main[rows][columns], int):
                        parking_main.append((rows, columns))
                        # parking_main.append(( matrix_main[rows][columns],(rows,columns)))

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
                print_main(matrix_main, matrix_free, matrix_bool, parking_main, airports_main, events_main)
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
            print("Case", cant_event, ":", "Yes")
            print(formatted + "\n")
        else:
            print("Case", cant_event, ":", "No" + "\n")

        cant_event += 1


if __name__ == '__main__':
    main()
