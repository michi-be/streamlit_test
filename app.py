import streamlit as st
import pandas as pd
import re   
import os
import string
import plotly.express as px

from dotenv import load_dotenv
import openai   


def get_current_dir():
    return os.path.dirname(os.path.abspath(__file__))

def get_dataset_path():
    
    csv_path = os.path.join(get_current_dir(), "data", "customer_reviews.csv")
    return csv_path

def clean_text(text):
    """Remove punctuation, convert to lowercase, and strip whitespace from text."""
    text = text.lower()
    text = text.strip()
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text


st.title("Hello GenAI")
st.write("This is your GenAI-powered data processing app!")

col1, col2 = st.columns(2)

with col1:
    if st.button("Ingest Data"):
        try:
            csv_path = get_dataset_path()
            st.session_state["df"] = pd.read_csv(csv_path)
            st.success("Data ingested successfully!")
        except FileNotFoundError:
            st.error("Dataset not found. Please check the path.")

with col2:
    if st.button("Parse Reviews"):
        if "df" in st.session_state:
            st.session_state["df"]["CLEANED_SUMMARY"] = st.session_state["df"]["SUMMARY"].apply(clean_text)
            st.success("Reviews parsed and cleaned!")
        else:
            st.warning("Please ingest data first.")

if "df" in st.session_state:
    st.subheader("🔍 Filter by Product")
    product = st.selectbox("Choose Product:", ["All Products"] + list( st.session_state["df"]["PRODUCT"].unique()) )

    st.subheader(f"🗂 Dataset Preview")
    
    if product != "All Products":
        filtered_df = st.session_state["df"][st.session_state["df"]["PRODUCT"] == product]
    else:
        filtered_df = st.session_state["df"]
    st.dataframe(filtered_df)

    st.subheader("📊 Sentiment Score by Product")
    grouped = st.session_state["df"].groupby("PRODUCT")["SENTIMENT_SCORE"].mean()
    st.bar_chart(grouped)

    st.subheader("Plotly Chart")
    fig = px.histogram(st.session_state["df"], x="SENTIMENT_SCORE", nbins=20, title="Sentiment Score Distribution")
    fig.update_layout(bargap=0.2, xaxis_title="Sentiment Score", yaxis_title="Count", showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

