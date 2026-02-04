import streamlit as st
from annotated_text import annotated_text
import ast
import pandas as pd
import random

## process data
df = pd.read_csv('data.csv', encoding='utf-8')
questions = (df['Question']).tolist()

bin_columns = [col for col in df.columns if col.endswith('-bin')]
open_columns = [col for col in df.columns if col.endswith('-open')]

# Main app
st.header("Six PhD cadidates in the Humanities reacting to seven (awkward) statements about doing a PhD")

# Process each question
for i, question in enumerate(questions):
    st.write(f"### {question}")
    
    # Count Yes and No responses for this question (row)
    yes_count = 0
    no_count = 0
    
    for col in bin_columns:
        response = df.loc[i, col]
        if response == 'Yes':
            yes_count += 1
        elif response == 'No':
            no_count += 1
    
    total = yes_count + no_count
    
    # Display the counts
    col1, col2, col3 = st.columns([2, 2, 6])
    with col1:
        st.metric("Yes", yes_count)
    with col2:
        st.metric("No", no_count)
    
    # Create a visual scale using progress bar
    if total > 0:
        yes_percentage = yes_count / total
        st.progress(yes_percentage, text=f"{yes_count} Yes  |  {no_count} No")
    
    # Get all open responses for this question
    open_responses = []
    for col in open_columns:
        response = df.loc[i, col]
        if pd.notna(response) and response.strip():  # Check if not empty
            open_responses.append(response)
    
    # Select and display two random responses
    if len(open_responses) >= 2:
        selected_responses = random.sample(open_responses, 2)
        st.write("**Selected responses:**")
        for resp in selected_responses:
            st.markdown(f'<p style="color:#2F4F2F; font-style:italic;">"{resp}"</p>', unsafe_allow_html=True)
    elif len(open_responses) == 1:
        st.write("**Selected response:**")
        st.markdown(f'<p style="color:#2F4F2F; font-style:italic;">"{open_responses[0]}"</p>', unsafe_allow_html=True)
    
    st.divider()