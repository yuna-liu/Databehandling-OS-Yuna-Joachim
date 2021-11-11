# Functions for analyzing and extracting interesting data

# Load libraries
import pandas as pd

# Count medals function with arbitrary number of arguments
def count_medals_n(df_orig, *arg):
    """
    Gives back number of medals groupby several attributes: *arg

    Input:
        df_orig: DataFrame
        *arg: column to get number of "Medal"
    
    Returns:
        df_best: new DataFrame
    """
    # Remove all NaN (no medal won == NaN)
    df_medals = df_orig[df_orig['Medal'].notna()]
    
    # count medals by column_name

    args_list = list(arg)
    args_list.append("Medal")
    df_medals = df_medals.groupby(args_list).count().reset_index()

    # "ID" column stands for the sum of medals
    args_list.append("ID")
    df_medals = df_medals.loc[:, args_list]
    
    # Changes dataframe from long to wide
    args = list(arg)
    df_medals = df_medals.pivot(index=args, columns="Medal", values="ID")

    # replace all NAs by 0
    df_medals.fillna(0, inplace=True)

    # generate Total, avoid using for-loop in pandas dataframe
    df_medals["Total"] = df_medals["Gold"] + df_medals["Silver"] + df_medals["Bronze"]
    
    # change type and change indeces to columns
    df_medals = df_medals.astype(int).reset_index(inplace=False)

    # Give back new dataframe
    return df_medals
