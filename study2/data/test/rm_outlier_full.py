from pandas import read_csv, DataFrame
from os import getcwd

##########################################################################################
def get_task_data():
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
        print(res)
        group[target_column] = group[target_column].apply(lambda x: mean_value if x < lower_bound or x > upper_bound else x)
        return group

    # Apply the function to each subgroup
    return df.groupby(group_columns).apply(replace).reset_index(drop=True)



df = get_task_data()
print(df)

df = replace_outliers_within_group(df, ['condition', 'posture'], "mt")

# write new dataframe to csv file
dest_path = getcwd() + "\\study2\\data\\test\\mt_full_no_outlier.csv"
df.to_csv(dest_path, index=False)