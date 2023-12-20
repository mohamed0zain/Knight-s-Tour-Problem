import random

def create_individual(n):
    # Create an individual as a random permutation of indices from 0 to n^2 - 1
    return random.sample(range(n * n), n * n)

def fitness(individual, n):
    # Calculate the fitness of an individual based on the number of knight attacks
    board = [[0] * n for _ in range(n)]
    moves = [(i // n, i % n) for i in individual]

    for i, (x, y) in enumerate(moves):
        board[x][y] = i

    attack_count = 0
    for i in range(n):
        for j in range(n):
            for dx, dy in [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)]:
                if 0 <= i + dx < n and 0 <= j + dy < n:
                    if abs(board[i][j] - board[i + dx][j + dy]) == 1:
                        attack_count += 1

    # Penalize solutions based on the number of attacks
    return n * n - attack_count

def crossover(parent1, parent2):
    # Use two-point crossover to create a child from two parents
    crossover_points = sorted(random.sample(range(len(parent1)), 2))
    child = parent1[:crossover_points[0]] + parent2[crossover_points[0]:crossover_points[1]] + parent1[crossover_points[1]:]
    return child

def mutate(individual, mutation_rate):
    # Apply mutation by swapping two genes with a certain probability for each gene
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            j = random.randint(0, len(individual) - 1)
            individual[i], individual[j] = individual[j], individual[i]
    return individual

def tournament_selection(population, tournament_size):
    # Perform tournament selection to choose individuals for crossover
    tournament = random.sample(population, tournament_size)
    return min(tournament, key=lambda x: fitness(x, int(len(x)**0.5)))

def genetic_algorithm(n, population_size=100, generations=1000, mutation_rate=0.01, tournament_size=5):
    # Execute the genetic algorithm to find a solution to the Knight's Tour problem
    population = [create_individual(n) for _ in range(population_size)]
    best_solution = None
    best_fitness = float('inf')

    for generation in range(generations):
        population = sorted(population, key=lambda x: fitness(x, n))
        new_population = [population[i] for i in range(population_size // 2)]

        for _ in range(population_size // 2):
            parent1 = tournament_selection(population, tournament_size)
            parent2 = tournament_selection(population, tournament_size)
            child = crossover(parent1, parent2)
            child = mutate(child, mutation_rate)
            new_population.append(child)

        population = new_population

        current_best = min(population, key=lambda x: fitness(x, n))
        current_fitness = fitness(current_best, n)

        if current_fitness < best_fitness:
            best_solution = current_best
            best_fitness = current_fitness

        print(f"Generation {generation}, Best Fitness: {best_fitness}")

        # If a perfect solution is found, break the loop
        if best_fitness == 0:
            break

    # Convert best solution to a 2D list representing the board
    board = [[-1 for _ in range(n)] for _ in range(n)]
    for i, idx in enumerate(best_solution):
        x, y = divmod(idx, n)
        board[x][y] = i

    return board, best_solution, best_fitness  # Return best_solution and best_fitness
