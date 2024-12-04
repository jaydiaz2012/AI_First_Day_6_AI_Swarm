!pip install matplotlib 
!pip install seaborn 
!pip install streamlit 
!pip install openai
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from openai import ChatCompletion
import openai
from swarm import SwarmAgent

# Configure API Keys
OPENAI_API_KEY = ""
openai.api_key = OPENAI_API_KEY

# Load dataset
def load_dataset(file):
    try:
        return pd.read_csv(file)
    except Exception as e:
        st.error(f"Error loading dataset: {e}")
        return None

# Analyze dataset
def analyze_dataset(df):
    summary = {
        "overview": df.describe(include="all").to_dict(),
        "null_values": df.isnull().sum().to_dict(),
        "correlations": df.corr().to_dict(),
    }
    return summary

# Advanced analysis using Swarm
def advanced_analysis(df):
    try:
        prompt = (
            "Perform clustering, detect anomalies, and provide predictive trends "
            f"on this e-commerce dataset:\n{df.to_csv(index=False)}"
        )
        response = openai.ChatCompletion.create(
            model="gpt-40-mini",
            messages=[
                {"role": "system", "content": "You are a data analysis assistant using Swarm."},
                {"role": "user", "content": prompt}
            ],
        )
        return response.choices[0].message['content']
    except Exception as e:
        st.error(f"Error performing advanced analysis: {e}")
        return None

# Visualize data
def visualize_data(df):
    visualizations = {}
    
    # Category Distribution
    plt.figure(figsize=(10, 6))
    sns.countplot(x='source', data=df)
    plt.title("Source Distribution")
    visualizations['category_distribution'] = plt.gcf()
    plt.close()

    # Monthly Sales Trends
    plt.figure(figsize=(10, 6))
    sns.barplot(x="date", y="revenue", data=df)
    plt.title("Monthly Sales Trends")
    visualizations['monthly_sales_trends'] = plt.gcf()
    plt.close()
    
    return visualizations

# Generate business insights
def generate_insights(summary, model):
    prompt = (
        f"Here is the dataset summary:\n{summary}\n"
        "Generate actionable business insights from the above dataset."
    )
    response = model.create(
        engine="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a data analyst AI."},
            {"role": "user", "content": prompt}
        ],
    )
    return response.choices[0].message['content']

# Generate a report
def generate_report(insights, advanced_analysis_result, file_path="report.txt"):
    with open(file_path, "w") as file:
        file.write("Automated Business Insights Report\n")
        file.write("=" * 50 + "\n\n")
        file.write("**Insights:**\n")
        file.write(insights + "\n\n")
        file.write("**Advanced Analysis:**\n")
        file.write(advanced_analysis_result + "\n")
    return file_path

# Streamlit App
def app():
    st.title("AI-Powered E-commerce Data Analyzer with Swarm")
    st.write("Upload your dataset to analyze, visualize, and generate advanced business insights.")

    # File upload
    uploaded_file = st.file_uploader("Upload CSV file", type="csv")
    if uploaded_file:
        df = load_dataset(uploaded_file)
        if df is not None:
            st.write("### Dataset Preview")
            st.dataframe(df.head())

            # Dataset Analysis
            st.write("### Dataset Analysis")
            summary = analyze_dataset(df)
            st.json(summary)

            # Advanced Analysis
            st.write("### Advanced Analysis (Clustering, Anomalies, Trends)")
            advanced_analysis_result = advanced_analysis(df)
            st.text_area("Advanced Analysis Results", advanced_analysis_result, height=300)

            # Data Visualizations
            st.write("### Data Visualizations")
            visualizations = visualize_data(df)
            for title, fig in visualizations.items():
                st.write(title.replace('_', ' ').title())
                st.pyplot(fig)

            # Business Insights
            st.write("### Business Insights")
            model = ChatCompletion(api_key=OPENAI_API_KEY)
            insights = generate_insights(summary, model)
            st.text_area("Insights", insights, height=200)

            # Download Report
            if st.button("Download Report"):
                report_path = generate_report(insights, advanced_analysis_result)
                with open(report_path, "rb") as file:
                    st.download_button(
                        label="Download Report",
                        data=file,
                        file_name="business_insights_report.txt",
                        mime="text/plain"
                    )

# Run Streamlit App
if __name__ == "__main__":
    app()
