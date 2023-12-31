import math
import random

def start():
    filename = input("Filename: ")
    f = open(filename, "r")
    data = read_data(f)

    n_exp = 10
    n = 10
    k = 10

    print(f"No. of experiments: {n_exp}")
    print(f"No. of iterations per experiment: {n}")
    print(f"No. of iterations in Tabu: {k}")

    best_solutions = []
    for i in range(n_exp):
        solution = run(n, k, data)
        best_solutions.append(solution)

    best = best_solutions[0]
    bestd = distance(best, data)
    sum = 0
    count = 0
    for sol in best_solutions:
        dst = distance(sol, data)
        sum += dst
        count += 1
        if dst < bestd:
            best = sol
            bestd = dst
        print(string_solution(sol, dst))
        
    print("---")
    print("BEST SOLUTION")
    print(string_solution(best, bestd))
    print(f"Average distance - {round(sum/count)}")
    print("---")

def read_data(file):
    for i in range(6):
        file.readline()

    data = []

    line = file.readline()
    while True:
        stripped_line = " ".join(line.split())
        if stripped_line == 'EOF':
            break
        item = tuple(map(int, stripped_line.split(" ")))
        data.append(item)
        line = file.readline()

    return data

def run(n, k, data):
    s0 = generate_random_solution(data)
    best = s0
    bcandidate = s0
    M = []
    Mf = []
    M.append(s0)
    Mf.append(k)

    for i in range(n):
        neighbours = generate_neighbours_of_solution(bcandidate, data)

        if not neighbours:
            continue

        bcandidate = neighbours[0]
        for j in range(len(neighbours)):
            isTabu = False
            for item in M:
                if neighbours[j] == item:
                    isTabu = True
                    break

            if isTabu:
                continue

            if distance(neighbours[j], data) < distance(bcandidate, data):
                bcandidate = neighbours[j]

        if distance(bcandidate, data) < distance(best, data):
            best = bcandidate

        to_remove = []
        for j in range(len(Mf)):
            Mf[j] = Mf[j] - 1
            if Mf[j] == 0:
                to_remove.append(j)
                M.pop(j)
        for j in to_remove:
            Mf.pop(j)

        M.append(bcandidate)
        Mf.append(k)

    return best

def generate_random_solution(data):
    solution = []
    for i in range(len(data)):
        solution.append(data[i][0])
    random.shuffle(solution)

    return solution

def generate_neighbours_of_solution(solution, data):
    neighbours = []
    for i in range(len(solution)):
        for j in range(i, len(solution)):
            neighbour = solution.copy()
            aux = neighbour[i]
            neighbour[i] = neighbour[j]
            neighbour[j] = aux
            neighbours.append(neighbour)

    return neighbours

def distance(solution, data):
    sum = 0
    for i in range(len(solution)):
        if i == len(solution) - 1:
            break
        sum += distance_between(solution[i], solution[i+1], data)
    
    return round(sum, 2)

def distance_between(A, B, data):
    return math.sqrt(pow(data[B-1][1]-data[A-1][1], 2) + pow(data[B-1][2]-data[A-1][2], 2))

def string_solution(solution, distance):
    return f"{solution} - distance: {distance}"

start()