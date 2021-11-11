# Functions for analyzing and extracting interesting data

# Load libraries
import pandas as pd


# count medals fct with arbitrary number of arguments
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
    #df_medals = df_medals.groupby([arg1, arg2, arg3, "Medal"]).count().reset_index()
  
    # Remove redundant columns, "Medal" is str column which is one level
    # "ID" column stands for the sum of medals
    args_list.append("ID")
    df_medals = df_medals.loc[:, args_list]
    
    # data long to wide
    args = list(arg)
    df_medals = df_medals.pivot(index=args, columns="Medal", values="ID")
    #df_medals = df_medals.pivot(index=[arg1, arg2, arg3], columns="Medal", values="ID")

    # replace all NAs by 0
    df_medals.fillna(0, inplace=True)

    # generate Total, avoid using for-loop in pandas dataframe
    df_medals["Total"] = df_medals["Bronze"] + df_medals["Gold"] + df_medals["Silver"]   
    
    # change type and change indices to columns
    df_medals = df_medals.astype(int)

    # sort medel descending
    df_medals = df_medals.sort_values("Total", ascending=False)

    # Give back new dataframe
    return df_medals