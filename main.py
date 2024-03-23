import streamlit as st
import openai
import json
import pandas as pd
import os


def extract_keywords(text):
    prompt = get_prompt_keywords() + text
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ],
    headers = {"Authorization": f"Bearer {os.environ.get('OPENAI_API_KEY')}"}
    )
    content = response.choices[0]['message']['content']
    try:
        data = json.loads(content)
        return pd.DataFrame(data["Key Phrases"], columns=["Key Phrases"])
    except (json.JSONDecodeError, KeyError):
        pass
    return pd.DataFrame(columns=["Key Phrases"])

def get_prompt_keywords():
    return '''Please extract key phrases from the following job description. 
      If you can't find relevant key phrases, return "". Do not make things up.    
        Always return your response as a valid JSON string. The format of that string should be this, 
        {
            "Key Phrases": ["Python programming", "Data analysis", "Machine learning", "Problem-solving"]
        }
    Job Description:
    ============
    '''

# Define columns
col1, col2 = st.columns([3, 2])

# Initialize DataFrame with default values
keywords = pd.DataFrame(columns=["Key Phrases"])



# Display UI components in the respective columns
with col1:
    st.title("Keywords Extraction")
    job_description = st.text_area("Paste your job description here", height=300)
    if st.button("Extract Keywords"):
        extracted_keywords = extract_keywords(job_description)

with col2:
    st.markdown("<br/>" * 5, unsafe_allow_html=True)
    if 'extracted_keywords' in locals():
        st.dataframe(extracted_keywords,
                     column_config={"Key Phrases": st.column_config.Column(width=300)},
                     hide_index=True
                     )


