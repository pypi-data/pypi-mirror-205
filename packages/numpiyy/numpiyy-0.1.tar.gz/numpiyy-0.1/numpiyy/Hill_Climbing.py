# import random

# # Define the objective function to optimize
# def objective_function(x, y):
#     return x**2 + y**2  # Example function: sum of squares

# # Define the hill climbing algorithm
# def hill_climbing(initial_state, step_size, objective_function):
#     current_state = initial_state
#     while True:
#         # Print current state coordinates
#         print(f"Current state: ({current_state[0]}, {current_state[1]})")

#         neighbors = []
#         # Generate neighboring states by perturbing current state
#         for i in range(len(current_state)):
#             new_state = list(current_state)
#             new_state[i] += random.uniform(-step_size, step_size)
#             neighbors.append(new_state)

#         # Find the best neighboring state
#         best_neighbor = min(neighbors, key=lambda state: objective_function(state[0], state[1]))

#         # If the best neighbor is worse than current state, terminate
#         if objective_function(best_neighbor[0], best_neighbor[1]) >= objective_function(current_state[0], current_state[1]):
#             print(f"Reached local minimum at: ({current_state[0]}, {current_state[1]})")
#             break

#         # Update current state to the best neighbor
#         current_state = best_neighbor

#     return current_state

# # Set initial state, step size, and run the hill climbing algorithm
# initial_state = [random.uniform(-5, 5), random.uniform(-5, 5)]  # Example initial state
# step_size = 0.1  # Example step size
# print(f"Initial state: ({initial_state[0]}, {initial_state[1]})")
# final_state = hill_climbing(initial_state, step_size, objective_function)
# print(f"Final state: ({final_state[0]}, {final_state[1]})")




import numpy as np

def find_neigbours(state, landscape):
    neighbours = []
    dim = landscape.shape
    if state[0]!=0:
        neighbours.append((state[0]-1,state[1]))
    if state[0] != dim[0] - 1:
        neighbours.append((state[0] + 1, state[1]))
    if state[1] != 0:
        neighbours.append((state[0], state[1] - 1))
    if state[1] != dim[1] - 1:
        neighbours.append((state[0], state[1] + 1))
    if state[0] != 0 and state[1] != 0:
        neighbours.append((state[0] - 1, state[1] - 1))
    if state[0] != 0 and state[1] != dim[1] - 1:
        neighbours.append((state[0] - 1, state[1] + 1))
    if state[0] != dim[0] - 1 and state[1] != 0:
        neighbours.append((state[0] + 1, state[1] - 1))
    if state[0] != dim[0] - 1 and state[1] != dim[1] - 1:
        neighbours.append((state[0] + 1, state[1] + 1))
    return neighbours

def hill_climb(curr_state, landscape):
    neighbours = find_neigbours(curr_state, landscape)
    bool
    ascended = False
    next_state = curr_state
    for neighbour in neighbours:
        if landscape[neighbour[0]][neighbour[1]]>landscape[next_state[0]][next_state[1]]:
            next_state = neighbour
            ascended = True
    return ascended, next_state


landscape = np.random.randint(1, high=50, size=(10,10))
print(landscape)
start_state = (5,7)
current_state = start_state
count = 1
ascending = True
while ascending:
   print("\nStep:- ", count)
   print("\nCurrent State Co-ordinates: ", current_state)
   print("\nCurrent State Value: ", landscape[current_state[0]][current_state[1]])
   count+=1
   ascending, current_state = hill_climb(current_state,landscape)
print("\nStep:- ", count)
print("\nCurrent State Co-ordinates: ", current_state)
print("\nCurrent State Value: ", landscape[current_state[0]][current_state[1]])