import random

SPRINT_DAYS = 14

def initialize_population(tasks, team_members, pop_size=50):
    population = []
    for _ in range(pop_size):
        assignment = {member: [] for member in team_members.keys()}
        for _, task in tasks.iterrows():
            eligible_members = [m for m, data in team_members.items() if task['project_id'] in data['Trained Projects']]
            if eligible_members:
                assigned_member = random.choice(eligible_members)
                if sum(tasks.loc[tasks['task_id'].isin(assignment[assigned_member]), 'task_hours']) + task[
                    'task_hours'] <= team_members[assigned_member]['Capacity'] * SPRINT_DAYS:
                    assignment[assigned_member].append(task['task_id'])
        population.append(assignment)
    return population


def fitness(assignment, tasks, team_members):
    total_utilization = 0
    for member, assigned_tasks in assignment.items():
        assigned_hours = sum(tasks.loc[tasks['task_id'].isin(assigned_tasks), 'task_hours'])
        max_capacity = team_members[member]['Capacity'] * SPRINT_DAYS
        if assigned_hours <= max_capacity:
            total_utilization += assigned_hours
    return total_utilization


def crossover(parent1, parent2):
    child = {member: [] for member in parent1.keys()}
    for member in parent1.keys():
        if random.random() > 0.5:
            child[member] = parent1[member][:]
        else:
            child[member] = parent2[member][:]
    return child


def mutate(assignment, tasks, team_members, mutation_rate=0.1):
    for member in assignment.keys():
        if random.random() < mutation_rate:
            if assignment[member]:
                task_to_move = random.choice(assignment[member])
                eligible_members = [m for m, data in team_members.items() if
                                    tasks.loc[tasks['task_id'] == task_to_move, 'project_id'].values[0] in data[
                                        'Trained Projects']]
                if eligible_members:
                    new_member = random.choice(eligible_members)
                    if sum(tasks.loc[tasks['task_id'].isin(assignment[new_member]), 'task_hours']) + \
                            tasks.loc[tasks['task_id'] == task_to_move, 'task_hours'].values[0] <= \
                            team_members[new_member]['Capacity'] * SPRINT_DAYS:
                        assignment[member].remove(task_to_move)
                        assignment[new_member].append(task_to_move)
    return assignment


def genetic_algorithm(tasks_df, team_df, generations=100, pop_size=50):
    team_members = {row['Team Member']: {'Trained Projects': list(map(int, str(row['Trained Projects']).split(', '))),
                                         'Capacity': row['Capacity']} for _, row in team_df.iterrows()}
    population = initialize_population(tasks_df, team_members, pop_size)

    for _ in range(generations):
        population = sorted(population, key=lambda x: fitness(x, tasks_df, team_members), reverse=True)
        new_population = population[:10]
        while len(new_population) < pop_size:
            parent1, parent2 = random.sample(population[:20], 2)
            child = crossover(parent1, parent2)
            child = mutate(child, tasks_df, team_members)
            new_population.append(child)
        population = new_population

    best_assignment = max(population, key=lambda x: fitness(x, tasks_df, team_members))
    utilization = fitness(best_assignment, tasks_df, team_members)
    print(f"Total Utilization: {utilization}")
    return best_assignment


import pandas as pd

# File paths
tasks_file = "tasks_300.csv"
team_file = "team_members.csv"

# Load datasets
tasks_data = pd.read_csv(tasks_file)
team_data = pd.read_csv(team_file)


# Running the algorithm
final_best_assignment = genetic_algorithm(tasks_data, team_data)


print("Final Utilization:")
for team_member_id, task_id in final_best_assignment.items():
    print(f"Team Member {team_member_id}:")
    task = tasks_data[tasks_data['task_id'].isin(task_id)]
    tm_utilization_total = task['task_hours'].sum()
    member_total_capacity = team_data[team_data['Team Member'] == team_member_id]['Capacity'] * SPRINT_DAYS
    print(tm_utilization_total)
    print(member_total_capacity)
    print(task.to_string(index=False))
    print("\n")