import random
import pandas as pd





def generate_data():

    # Define projects and team members
    projects = list(range(7))  # 7 projects indexed 0-6
    team_members = {
        1: {"trained_projects": {0, 1, 3, 5, 7}, "capacity": 4},
        2: {"trained_projects": {0, 1, 4, 5, 7}, "capacity": 5},
        3: {"trained_projects": {0, 1, 2, 4, 6}, "capacity": 7},
        4: {"trained_projects": {2, 3, 4, 6}, "capacity": 7},
        5: {"trained_projects": {1, 2, 5, 7}, "capacity": 7},
    }

    # Generate random tasks
    num_tasks = 200  # Number of tasks
    tasks = []

    for task_id in range(num_tasks):
        project_id = random.choice(projects)
        task_hours = random.randint(1, 30)  # Task duration in hours
        tasks.append({"task_id": task_id, "project_id": project_id, "task_hours": task_hours})

    # Create DataFrames
    team_members_df = pd.DataFrame([
        {"Team Member": tm, "Trained Projects": ", ".join(map(str, data["trained_projects"])),
         "Capacity": data["capacity"]}
        for tm, data in team_members.items()
    ])

    tasks_df = pd.DataFrame(tasks)

    # Save to CSV
    team_members_csv_path = "team_members.csv"
    tasks_csv_path = "tasks_300.csv"

    team_members_df.to_csv(team_members_csv_path, index=False)
    tasks_df.to_csv(tasks_csv_path, index=False)


if __name__ == '__main__':
    generate_data()