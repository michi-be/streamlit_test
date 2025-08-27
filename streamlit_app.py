import os
from dotenv import load_dotenv
import openai
import streamlit as st

@st.cache_data
def get_response(prompt, temperature):
    client = openai.Client()
    response = client.responses.create(
        model="gpt-4o",
        input=[{"role": "user", "content": prompt}],
        temperature=temperature,
        max_output_tokens=100
    )
    return response

# Load environment variables from .env file
load_dotenv()

st.title("Hello GenAI")
st.write("This is a simple Streamlit app to test OpenAI's GPT-4o model.")
userprompt = st.text_input("Enter your prompt:", "Explain generative AI in one sentence.")  
temperature = st.slider("Select creativity level (temperature):", 0.0, 1.0, 0.7)

client = openai.Client()
with st.spinner("Generating response..."):
    response =  get_response(userprompt, temperature)  

st.write(response.output[0].content[0].text)

