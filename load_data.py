import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly_express as px
import plotly.graph_objects as go
from datetime import datetime

## The clean data process OOP is inspired by the following referenes:
# 1. https://opendatascience.com/an-introduction-to-object-oriented-data-science-in-python/
# 2. https://stackoverflow.com/questions/69822737/is-oop-approach-towards-data-preprocessing-in-python-an-overkill


class ShowMeData:
    """The class is used for the intention to parse data, check missing data, clean missing data, and then export cleaned data"""
    def __init__(self, name, import_path="data/", export_path="data_clean/", sheet_name = None):
        self.name = name
        self.sheetname = sheet_name
        self.datatype = name.split(".")[-1]
        self.import_path = import_path
        self.export_path = export_path

    def parse_data(self): 
        if self.datatype == "csv":
            self.df = pd.read_csv(self.import_path+self.name)
        elif self.datatype == "xlsx":
            self.df = pd.read_excel(self.import_path+self.name, sheet_name=self.sheetname)
        return self.df

    def show_info(self):
        return f"""
        Dataframe info:\n{self.df.info()}

        Name: {self.name}

        Sheet name: {self.sheetname}

        Data head():\n{self.parse_data().head()}

        Shape: {self.df.shape}

        Index: {self.df.index}

        Columns: {self.df.columns}

        Variables types:\n{self.df.dtypes}
      
        Dataframe description:\n{self.df.describe()}

        Summary of missing values:\n{self.df.isnull().sum()}

        Total number of missing values:\n{self.df.isnull().sum().sum()}
        
        The percentage of missing values in each column:\n{self.df.isnull().sum()/self.df.shape[0]}  
        
        The variables that present null values the most:\n{(self.df.isnull().sum()/self.df.shape[0]).sort_values(ascending=False)[0:5]}

        
        """

      
    def main_pipe(self) -> pd.DataFrame:
        return (self.df
                 .dropna()
                 .reset_index(drop=True)
                 )
    
    def export_data(self) -> None:
        if self.datatype == "csv":
            self.df.to_csv(self.export_path+self.name, index=False)
        elif self.datatype == "xlsx":
            self.df.to_excel(self.export_path+self.name, sheet_name=self.sheetname)
        return None

    def process(self) -> None:
        self.parse_data()
        self.main_pipe()
        self.export_data()
        return None