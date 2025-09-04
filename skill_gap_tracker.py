import random
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# -----------------------
# 1. Generate Job Data
# -----------------------
job_roles = [
    "Data Analyst", "Machine Learning Engineer", "Data Scientist", 
    "Business Analyst", "AI Researcher", "Cloud Engineer",
    "Full Stack Developer", "Product Manager", "DevOps Engineer",
    "Data Engineer", "Cybersecurity Analyst", "Quantitative Analyst"
]

skills_pool = ["Python", "SQL", "Excel", "Tableau", "PowerBI", "Machine Learning",
               "Deep Learning", "Communication", "Project Management", "Leadership",
               "Data Cleaning", "Statistics", "Cloud Computing", "APIs", "Docker"]

# Generate 1000 job postings
jobs = []
for i in range(1000):
    job = random.choice(job_roles) + f" #{i+1}"
    num_skills = random.randint(5, 10)
    job_skills = random.sample(skills_pool, num_skills)
    required_levels = [random.randint(5, 10) for _ in range(num_skills)]
    for skill, level in zip(job_skills, required_levels):
        jobs.append({"Job": job, "Skill": skill, "Required_Level": level})

df_jobs = pd.DataFrame(jobs)

# -----------------------
# 2. User Skill Input
# -----------------------
user_skills = {}
all_skills = df_jobs['Skill'].unique()
print("Enter your skill levels (1-10) for the following skills:")
for skill in all_skills:
    while True:
        try:
            level = int(input(f"{skill}: "))
            if 1 <= level <= 10:
                user_skills[skill] = level
                break
            else:
                print("Enter a number between 1 and 10")
        except:
            print("Invalid input. Enter a number between 1 and 10")

# -----------------------
# 3. Choose Job
# -----------------------
print("\nChoose a job from the list below:")
unique_jobs = df_jobs['Job'].unique()
for idx, job in enumerate(unique_jobs[:50]):  # show first 50 jobs
    print(f"{idx+1}. {job}")

while True:
    try:
        choice = int(input("Enter the number of the job you want to see: "))
        if 1 <= choice <= len(unique_jobs[:50]):
            job_to_plot = unique_jobs[choice-1]
            break
        else:
            print("Invalid choice.")
    except:
        print("Enter a valid number.")

# -----------------------
# 4. Calculate Gap
# -----------------------
df_plot = df_jobs[df_jobs['Job'] == job_to_plot].copy()
df_plot['User_Level'] = df_plot['Skill'].map(user_skills)
df_plot['Gap'] = df_plot['Required_Level'] - df_plot['User_Level']
df_plot['Gap_Positive'] = df_plot['Gap'].apply(lambda x: x if x>0 else 0)

# -----------------------
# 5. Visualization
# -----------------------

# Radar Chart
fig_radar = go.Figure()
fig_radar.add_trace(go.Scatterpolar(
      r=df_plot['User_Level'],
      theta=df_plot['Skill'],
      fill='toself',
      name='Your Skill'
))
fig_radar.add_trace(go.Scatterpolar(
      r=df_plot['Required_Level'],
      theta=df_plot['Skill'],
      fill='toself',
      name='Required Skill'
))
fig_radar.update_layout(
  polar=dict(radialaxis=dict(visible=True, range=[0,10])),
  title=f"Skill Gap Radar for {job_to_plot}"
)
fig_radar.show()

# Horizontal Bar Chart
fig_bar = px.bar(df_plot, x='Gap_Positive', y='Skill', orientation='h',
                 title=f"Skill Gap for {job_to_plot}",
                 color='Gap_Positive', color_continuous_scale='reds')
fig_bar.show()

# Bubble Chart
fig_bubble = px.scatter(df_plot, x='Skill', y='Required_Level',
                        size='Gap_Positive', color='Gap_Positive',
                        title=f"Skill Gap Bubble Chart for {job_to_plot}",
                        size_max=50, color_continuous_scale='oranges')
fig_bubble.show()
