import numpy as np

# Define the probabilities of producing i new neutrons
p = []
for i in range(1, 4):
    p.append(0.2126 * 0.5893 ** (i - 1))
p.insert(0, 1 - sum(p))
print(p)

# Number of generations
num_generations = 10

# Number of simulations
num_simulations = 10000

# Initialize counts for each number of neutrons in each generation
counts = [[0 for j in range(5)] for i in range(num_generations)]

# Simulate the production of new neutrons for each generation
for _ in range(num_simulations):
    # Start with one neutron in the first generation
    num_neutrons = 1
    for generation in range(num_generations):
        new_neutrons = 0
        for _ in range(num_neutrons):
            # Count the number of new neutrons produced
            new_neutrons += np.random.choice(range(4), p=p)
        # Update the number of neutrons for the next generation
        num_neutrons = new_neutrons
        # Increment the count for the number of neutrons produced
        if num_neutrons <= 4:
            counts[generation][num_neutrons] += 1
            
# Calculate probabilities for each number of neutrons in each generation
probabilities = [[count / num_simulations for count in generation] for generation in counts]

# Output probabilities for each generation
for generation in range(num_generations):
    print(f"Generation {generation+1}:")
    for i, prob in enumerate(probabilities[generation]):
        print(f"p[{i+1}] = {prob:.4f}")

# Write the probabilities to a file
with open('output_task1.txt', 'w') as f:
    for generation in range(num_generations):
        f.write(f"Generation-{generation+1}:\n")
        for i, prob in enumerate(probabilities[generation]):
            f.write(f"p[{i+1}] = {prob:.4f}\n")
        f.write("\n")