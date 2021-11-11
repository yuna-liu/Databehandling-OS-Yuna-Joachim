# Functions for analyzing and extracting interesting data

# Load libraries
import pandas as pd


# Functions

def count_medals(df_orig, column_name):
    """
    Gives back number of medals per any attribute

    Input:
        df_orig: DataFrame
        column_name: column to get number of medals of each
    
    Returns:
        df_best: new DataFrame
    """
    
    # Remove redundant columns first
    df_medals = df_orig.drop(
        [column for column in df_orig.columns if (column != "Medal") and (column != column_name)],
        axis="columns"
    )

    # Remove all NaN (no medal won == NaN)
    df_medals = df_medals.dropna(axis="rows")

    # Add a counter-columns for number of ALL medals
    df_medals["Number medals"] = 1

    # Add counters of Gold, silver, and bronze medals
    for medal in df_medals["Medal"].unique():
        df_medals[f"Number {medal}"] = 0
        df_medals[f"Number {medal}"].loc[df_medals["Medal"] == medal] = 1

    # Groupby chosen column_name and count all number of medals
    df_medals = df_medals.groupby(column_name).sum()

    # Give back new dataframe
    return df_medals



# Functions count_medals_test does not produce warning

def df_count_medals(df_orig, column_name):
    """
    Gives back number of medals per any attribute

    Input:
        df_orig: DataFrame
        column_name: column to get number of medals of each
    
    Returns:
        df_best: new DataFrame
    """
    # Remove all NaN (no medal won == NaN)
    df_medals = df_orig[df_orig['Medal'].notna()]
    
    # count medals by column_name
    df_medals = df_medals.groupby([column_name, "Medal"]).count().reset_index()
  
    # Remove redundant columns, "Medal" is str column which is one level
    # "ID" column stands for the sum of medals

    df_medals = df_medals.loc[:, [column_name, "Medal", "ID"]]
    
    # data long to wide
    df_medals = df_medals.pivot(index=column_name, columns="Medal", values="ID")
    
    # replace all NAs by 0
    df_medals.fillna(0, inplace=True)

    # generate Total, avoid using for-loop in pandas dataframe
    df_medals["Total"] = df_medals["Bronze"] + df_medals["Gold"] + df_medals["Silver"]   
    
    # change type
    df_medals = df_medals.astype("int64")

    # sort medel descending
    df_medals = df_medals.sort_values("Total", ascending=False).head(10)

    # Give back new dataframe
    return df_medals

# Functions count_medals_test does not produce warning





# def function to count medals by year 
def count_medals_by_year(df_orig, column_name=None):
    """
    Gives back number of medals per any attribute

    Input:
        df_orig: DataFrame
        column_name: column to get number of medals of each
    
    Returns:
        df_best: new DataFrame
    """
    # Remove all NaN (no medal won == NaN)
    df_medals = df_orig[df_orig['Medal'].notna()]
    
    # count medals by column_name
    df_medals = df_medals.groupby(["Year", column_name,  "Medal"]).count().reset_index()
  
    # Remove redundant columns, "Medal" is str column which is one level
    # "ID" column stands for the sum of medals

    df_medals = df_medals.loc[:, ["Year", column_name, "Medal", "ID"]]
    
    # data long to wide
    df_medals = df_medals.pivot(index=["Year", column_name], columns="Medal", values="ID")
    
    # replace all NAs by 0
    df_medals.fillna(0, inplace=True)

    # generate Total, avoid using for-loop in pandas dataframe
    df_medals["Total"] = df_medals["Bronze"] + df_medals["Gold"] + df_medals["Silver"]   
    
    # change type
    df_medals = df_medals.astype("int64")

    # some index are missing, so:
    df_medals = df_medals.reset_index()

    # set name to index
    df_medals.index.names = ["ID"]
    
    # sort medel descending
    df_medals = df_medals.sort_values("Total", ascending=False).head(10)

    # Give back new dataframe
    return df_medals









# def fct for each country
def count_medals_by_country(df_orig, column_name=None):
    """
    Gives back number of medals per any attribute

    Input:
        df_orig: DataFrame
        column_name: column to get number of medals of each
    
    Returns:
        df_best: new DataFrame
    """
    # Remove all NaN (no medal won == NaN)
    df_medals = df_orig[df_orig['Medal'].notna()]
    
    # count medals by column_name
    df_medals = df_medals.groupby(["region", column_name,  "Medal"]).count().reset_index()
  
    # Remove redundant columns, "Medal" is str column which is one level
    # "ID" column stands for the sum of medals

    df_medals = df_medals.loc[:, ["region", column_name, "Medal", "ID"]]
    
    # data long to wide
    df_medals = df_medals.pivot(index=["region", column_name], columns="Medal", values="ID")
    
    # replace all NAs by 0
    df_medals.fillna(0, inplace=True)

    # generate Total, avoid using for-loop in pandas dataframe
    df_medals["Total"] = df_medals["Bronze"] + df_medals["Gold"] + df_medals["Silver"]   
    
    # change type
    df_medals = df_medals.astype("int64")
    
    # some index are missing, so:
    df_medals = df_medals.reset_index()
    
    
    # set name to index
    df_medals.index.names = ["ID"]



    # sort medel descending
    df_medals = df_medals.sort_values("Total", ascending=False).head(10)

    # Give back new dataframe
    return df_medals





# def fct for each country each year
def count_medals_by_country_by_year(df_orig, column_name=None):
    """
    Gives back number of medals per any attribute

    Input:
        df_orig: DataFrame
        column_name: column to get number of medals of each
    
    Returns:
        df_best: new DataFrame
    """
    # Remove all NaN (no medal won == NaN)
    df_medals = df_orig[df_orig['Medal'].notna()]
    
    # count medals by column_name
    df_medals = df_medals.groupby(["Year", "region", column_name,  "Medal"]).count().reset_index()
  
    # Remove redundant columns, "Medal" is str column which is one level
    # "ID" column stands for the sum of medals

    df_medals = df_medals.loc[:, ["Year", "region", column_name, "Medal", "ID"]]
    
    # data long to wide
    df_medals = df_medals.pivot(index=["Year", "region", column_name], columns="Medal", values="ID")
    
    # replace all NAs by 0
    df_medals.fillna(0, inplace=True)

    # generate Total, avoid using for-loop in pandas dataframe
    df_medals["Total"] = df_medals["Bronze"] + df_medals["Gold"] + df_medals["Silver"]   
    
    # change type
    df_medals = df_medals.astype("int64")
    
    # some index are missing, so:
    df_medals = df_medals.reset_index()

    # set name to index
    df_medals.index.names = ["ID"]

    
    # sort medel descending
    df_medals = df_medals.sort_values("Total", ascending=False).head(10)

    # Give back new dataframe
    return df_medals




# try def fct with several arguments, but failed
def count_medals_args(df_orig, *args):
    """
    Gives back number of medals per any attribute

    Input:
        df_orig: DataFrame
        column_name: column to get number of medals of each
    
    Returns:
        df_best: new DataFrame
    """
    # Remove all NaN (no medal won == NaN)
    df_medals = df_orig[df_orig['Medal'].notna()]
    
    # count medals by column_name
    args_list = list(args)
    args_list.append("Medal")
    df_medals = df_medals.groupby(args).count().reset_index()
  
    # Remove redundant columns, "Medal" is str column which is one level
    # "ID" column stands for the sum of medals
    args_list.append("ID")
    df_medals = df_medals.loc[:, args_list]
    
    # data long to wide
    df_medals = df_medals.pivot(index=list(args), columns="Medal", values="ID")
    
    # replace all NAs by 0
    df_medals.fillna(0, inplace=True)

    # generate Total, avoid using for-loop in pandas dataframe
    df_medals["Total"] = df_medals["Bronze"] + df_medals["Gold"] + df_medals["Silver"]   
    
    # change type
    df_medals = df_medals.astype("int64")

    # sort medel descending
    df_medals = df_medals.sort_values("Total", ascending=False).head(10)

    # Give back new dataframe
    return df_medals


