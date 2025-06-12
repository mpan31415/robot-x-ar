from pandas import read_csv, DataFrame
from os import getcwd

##########################################################################################
def get_raw_data():
    my_file_dir = getcwd() + "\\study2\\data\\test\\mt_full.csv"
    df = read_csv(my_file_dir)
    return df

##########################################################################################
def replace_outliers_within_group(df:DataFrame, group_columns:list, target_column:str):
    # Reset index to ensure group_columns are not in the index
    df = df.reset_index(drop=True)

    # Function to calculate and replace outliers within each group
    def replace(group):
        Q1 = group[target_column].quantile(0.25)
        Q3 = group[target_column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        mean_value = group[(group[target_column] >= lower_bound) & (group[target_column] <= upper_bound)][target_column].mean()
        res = group[(group[target_column] >= lower_bound) & (group[target_column] <= upper_bound)][target_column].count()
        print(f"[replace_outliers_within_group] Number of outliers: {len(group)-res}/{len(group)}")
        print(f"[replace_outliers_within_group] Mean value for replacement: {mean_value}")
        group[target_column] = group[target_column].apply(lambda x: mean_value if x < lower_bound or x > upper_bound else x)
        return group

    # Apply the function to each subgroup
    return df.groupby(group_columns).apply(replace).reset_index(drop=True)


##########################################################################################
def replace_outliers(df:DataFrame, target_column:str):
    # Reset index to ensure group_columns are not in the index
    df = df.reset_index(drop=True)

    Q1 = df[target_column].quantile(0.25)
    Q3 = df[target_column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    mean_value = df[(df[target_column] >= lower_bound) & (df[target_column] <= upper_bound)][target_column].mean()
    res = df[(df[target_column] >= lower_bound) & (df[target_column] <= upper_bound)][target_column].count()
    print(f"[replace_outliers] Number of outliers: {len(df)-res}/{len(df)}")
    print(f"[replace_outliers] Mean value for replacement: {mean_value}")
    df[target_column] = df[target_column].apply(lambda x: mean_value if x < lower_bound or x > upper_bound else x)
    return df



df = get_raw_data()
print(df.head())


################### remove outliers altogether ###################
df1 = replace_outliers(df, "mt")
dest_path1 = getcwd() + "\\study2\\data\\test\\mt_no_outlier_all.csv"
df1.to_csv(dest_path1, index=False)


################### remove outlier grouped by condition ###################
df2 = replace_outliers_within_group(df, ['condition'], "mt")
dest_path2 = getcwd() + "\\study2\\data\\test\\mt_no_outlier_by_cond.csv"
df2.to_csv(dest_path2, index=False)
