import pandas as pd
from backend.llm import get_llm


class DataAgent:

    def __init__(self):
        self.llm = get_llm()

    def analyze_csv(self, file_path: str):

        df = pd.read_csv(file_path)

        data_summary = f"""
        Dataset Shape: {df.shape}
        Columns: {list(df.columns)}
        Data Types:
        {df.dtypes.to_string()}

        First 5 Rows:
        {df.head().to_string()}

        Missing Values:
        {df.isnull().sum().to_string()}

        Statistical Summary:
        {df.describe(include='all').to_string()}
        """

        prompt = f"""
        You are an expert Data Analysis Agent.

        Analyze this dataset information:

        {data_summary}

        Provide:
        1. Dataset Overview
        2. Important Patterns
        3. Missing Data Analysis
        4. Key Insights
        5. Suggestions

        Explain everything in simple language.
        """

        response = self.llm.invoke(prompt)

        return response.content