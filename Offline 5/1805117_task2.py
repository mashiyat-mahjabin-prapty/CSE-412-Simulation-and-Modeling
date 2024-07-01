import sys
import random
import numpy as np
import matplotlib.pyplot as plt

def conduct_interview(n, m, s, iterations=100000):
    success_count = 0
    for _ in range(iterations):
        scores = [random.uniform(0, 1) for _ in range(n)]
        selected_indices = random.sample(range(n), m)
        selected_scores = [scores[i] for i in selected_indices]
        threshold = max(selected_scores) if selected_scores else 0

        selected_index = next((i for i in range(n) if i not in selected_indices and scores[i] > threshold), n - 1)
        
        top_scorers = sorted(scores)[-s:]
        if scores[selected_index] in top_scorers:
            success_count += 1
            
    return success_count / iterations * 100

if __name__ == '__main__':
    n = 100
    success_criteria = [1, 3, 5, 10]

    for s in success_criteria:
        success_rate_list = [conduct_interview(n, m, s) for m in range(n)]
        
        plt.figure(figsize=(6, 6))
        plt.title(f'Success Rate vs. m\ns = {s}, n = {n}, 100000 iterations')
        plt.plot(range(n), success_rate_list)
        plt.xlabel('m')
        plt.ylabel('Success Rate')
        plt.savefig(f'1805117_task2_s{s}.png')
        plt.show()
