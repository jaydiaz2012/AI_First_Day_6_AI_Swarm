import pandas as pd
import openai
import matplotlib.pyplot as plt
from openai_swarm import SwarmAgent  
from firecrawl import FirecrawlAgent  

class WebAnalyticsAI:
    def __init__(self, framework="swarm", dataset_path=None):
        self.framework = framework
        self.dataset_path = dataset_path
        self.data = None
        self.agent = None

        if self.dataset_path:
            self.load_data()

        self.initialize_agent()

    def load_data(self):
        try:
            self.data = pd.read_csv(self.dataset_path)
            print(f"Dataset loaded successfully from {self.dataset_path}")
        except Exception as e:
            print(f"Error loading dataset: {e}")

    def initialize_agent(self):
        if self.framework.lower() == "swarm":
            self.agent = SwarmAgent(model="gpt-4o-mini")  # Adjust as per actual API
        elif self.framework.lower() == "firecrawl":
            self.agent = FirecrawlAgent(model="gpt-4o-mini")
        else:
            raise ValueError("Unsupported framework. Choose 'swarm' or 'firecrawl'.")
        print(f"Initialized agent using {self.framework} framework.")

    def analyze_data(self):
        if self.data is None:
            print("No dataset loaded for analysis.")
            return

        summary = self.data.describe()
        print("Dataset Summary:")
        print(summary)

        missing_data = self.data.isnull().sum()
        print("\nMissing Data Count:")
        print(missing_data)

    def generate_visualizations(self):
        if self.data is None:
            print("No dataset loaded for visualization.")
            return

        try:
            plt.figure(figsize=(10, 6))
            self.data["pageviews"].hist(bins=30)
            plt.title("Page Views Distribution")
            plt.xlabel("Page Views")
            plt.ylabel("Frequency")
            plt.show()
        except Exception as e:
            print(f"Error generating visualizations: {e}")

    def generate_insights(self):
        if self.data is None:
            print("No dataset loaded for insights generation.")
            return

        query = (
            "Analyze this web analytics dataset for patterns and generate actionable insights "
            "focusing on user engagement, traffic sources, and conversion rates."
        )
        
        try:
            insights = self.agent.query(query, data=self.data.to_dict())  # Adjust based on API
            print("Insights:")
            print(insights)
        except Exception as e:
            print(f"Error generating insights: {e}")

    def generate_report(self, output_path="report.txt"):
        if self.data is None:
            print("No dataset loaded for report generation.")
            return

        query = "Create a detailed business report from the given web analytics data."

        try:
            report = self.agent.query(query, data=self.data.to_dict())  # Adjust based on API
            with open(output_path, "w") as f:
                f.write(report)
            print(f"Report saved to {output_path}")
        except Exception as e:
            print(f"Error generating report: {e}")

if __name__ == "__main__":
    dataset_path = "https://raw.githubusercontent.com/jaydiaz2012/AI_First_Day_6_AI_Swarm/refs/heads/main/ai%20first%20sales%20data%20-%20sales%20(1).csv"

    # Create an instance of the WebAnalyticsAI class
    ai_agent = WebAnalyticsAI(framework="swarm", dataset_path=dataset_path)

    # Perform operations
    ai_agent.analyze_data()
    ai_agent.generate_visualizations()
    ai_agent.generate_insights()
    ai_agent.generate_report(output_path="business_insights_report.txt")
