# Project Title
A Metaheuristic based Approach to Maximize Sprint Capacity Utilization using Genetic Algorithm

The genetic algorithm was implemented to enhance the allocation of tasks for a team during a 14-day 
sprint. A total of 420 task hours were allocated across five team members. The calculated workload for 
each team member is shown along with their individual capacity limits. Each team member has been 
assigned solely tasks from projects for which they are qualified, following the established constraints.

# Dataset:
This Project needs two CSV files as input: 

```bash
  tasks_300.csv
```
 This file holds information about tasks, including task_id, project_id, and task_hours.
 ```bash
  team_members.csv
```
This file enumerates team members, detailing their trained projects and available capacity.
   
# Code Overview:
1.initialize_population: Creates an initial population of randomly generated task assignments.
 ```bash
  def initialize_population(tasks, team_members, pop_size=50):
    population = []
    for _ in range(pop_size):
        assignment = {member: [] for member in team_members.keys()}
        for _, task in tasks.iterrows():
            eligible_members = [m for m, data in team_members.items() if task['project_id'] in data['Trained Projects']]
            if eligible_members:
                assigned_member = random.choice(eligible_members)
                if sum(tasks.loc[tasks['task_id'].isin(assignment[assigned_member]), 'task_hours']) + task['task_hours'] <= team_members[assigned_member]['Capacity'] * SPRINT_DAYS:
                    assignment[assigned_member].append(task['task_id'])
        population.append(assignment)
    return population
```
    
    
2.fitness: Evaluate the efficiency of an assignment by calculating the total assigned hours while ensuring it does not exceed capacity.
 ```bash
  def fitness(assignment, tasks, team_members):
    total_utilization = 0
    for member, assigned_tasks in assignment.items():
        assigned_hours = sum(tasks.loc[tasks['task_id'].isin(assigned_tasks), 'task_hours'])
        max_capacity = team_members[member]['Capacity'] * SPRINT_DAYS
        if assigned_hours <= max_capacity:
            total_utilization += assigned_hours
    return total_utilization
```
  
    
3.crossover:  Merges two parent solutions to produce a new child solution.
 ```bash
  def crossover(parent1, parent2):
    child = {member: [] for member in parent1.keys()}
    for member in parent1.keys():
        if random.random() > 0.5:
            child[member] = parent1[member][:]
        else:
            child[member] = parent2[member][:]
    return child 
```
  
    
4.mutate:  Randomly alters assignments to foster diversity and enhance optimization.
 ```bash
  def mutate(assignment, tasks, team_members, mutation_rate=0.1):
    for member in assignment.keys():
        if random.random() < mutation_rate:
            if assignment[member]:
                task_to_move = random.choice(assignment[member])
                eligible_members = [m for m, data in team_members.items() if
                                    tasks.loc[tasks['task_id'] == task_to_move, 'project_id'].values[0] in data['Trained Projects']]
                if eligible_members:
                    new_member = random.choice(eligible_members)
                    if sum(tasks.loc[tasks['task_id'].isin(assignment[new_member]), 'task_hours']) + \
                            tasks.loc[tasks['task_id'] == task_to_move, 'task_hours'].values[0] <= \
                            team_members[new_member]['Capacity'] * SPRINT_DAYS:
                        assignment[member].remove(task_to_move)
                        assignment[new_member].append(task_to_move)
    return assignment
```
  
   
5.genetic_algorithm: Progresses through multiple generations, selecting the most effective solutions and implementing crossover and mutation.
 ```bash
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
```
  
   
6. Improt Dataset:
   # File paths

```bash
  tasks_file = "tasks_300.csv"
  team_file = "team_members.csv"
  ```
  

  # Load datasets
  ```bash
  tasks_data = pd.read_csv(tasks_file)
  team_data = pd.read_csv(team_file)
```
  
  
7.Final Utilization:
  # Running the algorithm

   ```bash
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
```
  

# Result: 
Every team member is utilized to their full potential as the hours assigned to tasks align with their 
overall capacity. The algorithm has successfully allocated tasks while preventing any member from 
being overwhelmed. Each individual is given tasks related to projects they are qualified for, based on 
the data provided. The constraints of the genetic algorithm made sure that tasks were assigned only 
to suitable team members. While utilization is at its peak, additional refinements in task allocation 
could enhance efficiency. The workload seems to be fairly balanced, with three members receiving 98 
hours, one member with 70 hours, and another with 56 hours.

 ```bash
  Total Utilization: 420
Final Utilization:
Team Member 1:
56
0    56
Name: Capacity, dtype: int64
 task_id  project_id  task_hours
      12           0          23
      19           5          24
      25           0           2
      53           0           5
      90           0           1
     113           3           1


Team Member 2:
70
1    70
Name: Capacity, dtype: int64
 task_id  project_id  task_hours
      22           0          28
      24           0          26
      33           4          14
      82           4           2


Team Member 3:
98
2    98
Name: Capacity, dtype: int64
 task_id  project_id  task_hours
       1           4          19
       2           2          25
       6           6          13
       7           1          26
      15           6           9
      37           4           5
      61           6           1


Team Member 4:
98
3    98
Name: Capacity, dtype: int64
 task_id  project_id  task_hours
       0           6          22
       3           6          20
       5           3          12
      11           6          18
      14           6          15
      31           3           9
      51           3           1
     119           4           1


Team Member 5:
98
4    98
Name: Capacity, dtype: int64
 task_id  project_id  task_hours
       4           1           5
       8           2          25
       9           2          27
      10           1           5
      16           5          18
      18           2           6
      20           1           3
      52           5           1
      72           2           2
     118           5           6 
```
   

