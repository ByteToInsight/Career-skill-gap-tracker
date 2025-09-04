import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Career Skill Gap Tracker", layout="wide")

# Example job dataset (can be replaced with your data generator)
job_title = "Data Analyst"
skills = ["Python", "SQL", "Excel", "Data Visualization", "Statistics"]
required_levels = [8, 7, 6, 7, 6]

# Initialize session_state for persistent input
if "user_levels" not in st.session_state:
    st.session_state.user_levels = {skill: 0 for skill in skills}

st.title("🚀 Career Skill Gap Tracker")
st.subheader(f"Job: {job_title}")

# Sidebar input
st.sidebar.markdown("### Enter Your Current Skill Levels:")
user_levels = []
for skill, req_level in zip(skills, required_levels):
    level = st.sidebar.select_slider(
        f"{skill} (required: {req_level})",
        options=list(range(0, 11)),
        format_func=lambda x: "⭐"*x if x > 0 else "0️⃣",
        key=skill
    )
    st.session_state.user_levels[skill] = level
    user_levels.append(level)

# Compute gap
gap = [req - usr for req, usr in zip(required_levels, user_levels)]

# ------------------- Layout -------------------
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📊 Skill Comparison Radar Chart")
    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=required_levels,
        theta=skills,
        fill='toself',
        name='Required'
    ))
    fig_radar.add_trace(go.Scatterpolar(
        r=user_levels,
        theta=skills,
        fill='toself',
        name='You'
    ))
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0,10])),
        showlegend=True
    )
    st.plotly_chart(fig_radar, use_container_width=True)

with col2:
    st.markdown("### 📊 Skill Gap Bar Chart")
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        x=skills,
        y=gap,
        marker_color='indianred',
        name="Gap"
    ))
    fig_bar.add_trace(go.Bar(
        x=skills,
        y=user_levels,
        marker_color='lightgreen',
        name="Your Level"
    ))
    fig_bar.update_layout(barmode='group', yaxis=dict(title="Skill Level"))
    st.plotly_chart(fig_bar, use_container_width=True)

# Overall completion
completion = sum(user_levels)/sum(required_levels)*100
st.markdown("### 🎯 Overall Skill Completion")
fig_donut = go.Figure(go.Pie(
    values=[sum(user_levels), sum(required_levels)-sum(user_levels)],
    labels=["You", "Gap"],
    hole=0.6,
    marker_colors=['lightgreen', 'lightcoral']
))
fig_donut.update_layout(showlegend=True)
st.plotly_chart(fig_donut, use_container_width=True)

st.markdown(f"**Overall Skill Completion:** {completion:.2f}%")
