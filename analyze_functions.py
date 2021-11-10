# Functions for analyzing and extracting interesting data

# Load libraries
import pandas as pd


# Functions

def count_medals(df_orig, column_name):
    """
    Gives back number of medals per any attribute

    Input:
        df_orig: DataFrame
        column_name: column to get top values of
    
    Returns:
        df_best: new DataFrame
    """
    
    # Remove all rows with NaNs (no medals are NaN)
    df_best = df_orig.dropna(axis="rows")

    # Adds a counter-column for number of medals
    df_best["Number medals"] = 1

    # Groupby chosen column_name
    # Count number of medals and sort by number of medals
    df_best = df_best.groupby(column_name).sum().sort_values("Number medals", ascending=False)
    
    # Remove redundant columns
    df_best = df_best.drop(
        [column for column in df_best.columns if column != "Number medals"],
        axis="columns"
    )

    # Give back new dataframe
    return df_best
