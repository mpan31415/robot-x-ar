from pandas import read_csv, DataFrame
from os import getcwd
from re import sub


NUM_PARTICIPANTS = 12

##########################################################################################
def get_demo_data():
    
    my_curr_dir = getcwd()
    my_file_dir = my_curr_dir + "\demographics\cleaned.csv"
    df = read_csv(my_file_dir)
    
    print("Finished reading demographics csv file!")
    
    return df

##########################################################################################
def get_raw_data():
    
    my_curr_dir = getcwd()
    my_file_dir = my_curr_dir + "\data\unity" + '\Results.csv'
    big_df = read_csv(my_file_dir)
    num_cols = big_df.shape[1]
    df = big_df.iloc[:, 17:num_cols]
    df = df.fillna(1)
    
    print("\n Finished reading raw csv file! \n")
    
    return df

####################################################################################
def remove_med_auto(df):
    index_med_auto = df[ (df['autonomy'] == 0.4) ].index
    df = df.drop(index_med_auto)
    return df

####################################################################################
def get_grouped_auto_list(auto_list):
    grouped_list = []
    for auto in auto_list:
        if auto > 0.4:
            grouped_list.append("high")
        else:
            grouped_list.append("low")
    return grouped_list

############################################################################################
def list_times_five(old_list):
    old_len = len(old_list)
    new_list = []
    for i in range(old_len):
        for j in range(5):
            new_list.append(old_list[i])
    return new_list


##########################################################################################
def preprocess_tlx():
    
    # get overall dataframe
    raw = get_raw_data()
    demo_df = get_demo_data()
    order_list = demo_df['order'].tolist()
    trust_tech_list = demo_df['trust_tech'].tolist()
    play_games_list = demo_df['play_games'].tolist()
    play_music_list = demo_df['play_music'].tolist()
    
    # get first 2 columns as lists
    part_id_list = raw.iloc[2:NUM_PARTICIPANTS*5+2, 0].tolist()
    for i in range(len(part_id_list)):
        part_id_list[i] = int(sub("P", "", part_id_list[i]))
    alpha_id_list_str = raw.iloc[2:NUM_PARTICIPANTS*5+2, 1].tolist()
    auto_id_list = [round(float(1.0 - float(alpha_id_list_str[i])/5.0), 1) for i in range(len(alpha_id_list_str))]
    
    # get lists for each tlx dimension
    tlx1_list = raw.iloc[2:NUM_PARTICIPANTS*5+2, 2].tolist()
    tlx2_list = raw.iloc[2:NUM_PARTICIPANTS*5+2, 3].tolist()
    tlx3_list = raw.iloc[2:NUM_PARTICIPANTS*5+2, 4].tolist()
    tlx4_list = raw.iloc[2:NUM_PARTICIPANTS*5+2, 5].tolist()
    tlx5_list = raw.iloc[2:NUM_PARTICIPANTS*5+2, 6].tolist()
    tlx6_list = raw.iloc[2:NUM_PARTICIPANTS*5+2, 7].tolist()
    
    tlx1_list = [float(tlx1_list[i]) for i in range(len(tlx1_list))]
    tlx2_list = [float(tlx2_list[i]) for i in range(len(tlx2_list))]
    tlx3_list = [float(tlx3_list[i]) for i in range(len(tlx3_list))]
    tlx4_list = [float(tlx4_list[i]) for i in range(len(tlx4_list))]
    tlx5_list = [float(tlx5_list[i]) for i in range(len(tlx5_list))]
    tlx6_list = [float(21.0 - float(tlx6_list[i])) for i in range(len(tlx6_list))]
    
    # get average values of TLX
    tlx_ave_list = []
    for i in range(len(tlx1_list)):
        this_row_list = [tlx1_list[i], tlx2_list[i], tlx3_list[i], tlx4_list[i], tlx5_list[i], tlx6_list[i]]
        tlx_ave = ave_of_list(this_row_list)
        tlx_ave_list.append(tlx_ave)
        
    grouped_auto_list = get_grouped_auto_list(auto_id_list)
    
    # generate new dataframe
    df_dict = {
        'pid': part_id_list,
        'trust_tech': list_times_five(trust_tech_list),
        'play_games': list_times_five(play_games_list),
        'play_music': list_times_five(play_music_list),
        'order': list_times_five(order_list),
        'autonomy': auto_id_list,
        'auto_grouped': grouped_auto_list,
        'tlx_mental': tlx1_list,
        'tlx_physical': tlx2_list,
        'tlx_hurried': tlx3_list,
        'tlx_insecure': tlx4_list,
        'tlx_hard': tlx5_list,
        'tlx_successful': tlx6_list,
        'tlx_ave': tlx_ave_list
    }
    tlx_df = DataFrame(df_dict)
    
    # write new dataframe to csv file
    dest_path = getcwd() + "\questionnaires\data" + '\\tlx_preprocessed.csv'
    tlx_df.to_csv(dest_path, index=False)
    
    tlx_df = remove_med_auto(tlx_df)
    # write new dataframe to csv file
    dest_path = getcwd() + "\dataframes" + '\\tlx.csv'
    tlx_df.to_csv(dest_path, index=False)
    
    print(" Successfully written pre-processed data to csv file! \n")


##########################################################################################
def preprocess_mdmt():
    
    # get overall dataframe
    raw = get_raw_data()
    demo_df = get_demo_data()
    order_list = demo_df['order'].tolist()
    trust_tech_list = demo_df['trust_tech'].tolist()
    play_games_list = demo_df['play_games'].tolist()
    play_music_list = demo_df['play_music'].tolist()
    
    # get first 2 columns as lists
    part_id_list = raw.iloc[2:NUM_PARTICIPANTS*5+2, 0].tolist()
    for i in range(len(part_id_list)):
        part_id_list[i] = int(sub("P", "", part_id_list[i]))
    alpha_id_list_str = raw.iloc[2:NUM_PARTICIPANTS*5+2, 1].tolist()
    auto_id_list = [round(float(1.0 - float(alpha_id_list_str[i])/5.0), 1) for i in range(len(alpha_id_list_str))]
    
    # get list for each mdmt dimension
    mdmt1_list = raw.iloc[2:NUM_PARTICIPANTS*5+2, 8].tolist()
    mdmt2_list = raw.iloc[2:NUM_PARTICIPANTS*5+2, 9].tolist()
    mdmt3_list = raw.iloc[2:NUM_PARTICIPANTS*5+2, 10].tolist()
    mdmt4_list = raw.iloc[2:NUM_PARTICIPANTS*5+2, 11].tolist()
    mdmt5_list = raw.iloc[2:NUM_PARTICIPANTS*5+2, 12].tolist()
    mdmt6_list = raw.iloc[2:NUM_PARTICIPANTS*5+2, 13].tolist()
    mdmt7_list = raw.iloc[2:NUM_PARTICIPANTS*5+2, 14].tolist()
    mdmt8_list = raw.iloc[2:NUM_PARTICIPANTS*5+2, 15].tolist()
    
    mdmt1_list = [float(mdmt1_list[i])-1 for i in range(len(mdmt1_list))]
    mdmt2_list = [float(mdmt2_list[i])-1 for i in range(len(mdmt2_list))]
    mdmt3_list = [float(mdmt3_list[i])-1 for i in range(len(mdmt3_list))]
    mdmt4_list = [float(mdmt4_list[i])-1 for i in range(len(mdmt4_list))]
    mdmt5_list = [float(mdmt5_list[i])-1 for i in range(len(mdmt5_list))]
    mdmt6_list = [float(mdmt6_list[i])-1 for i in range(len(mdmt6_list))]
    mdmt7_list = [float(mdmt7_list[i])-1 for i in range(len(mdmt7_list))]
    mdmt8_list = [float(mdmt8_list[i])-1 for i in range(len(mdmt8_list))]
    
    # get sub-group average lists
    reliable_ave_list = []
    capable_ave_list = []
    for i in range(len(mdmt1_list)):
        reliable_ave = float((mdmt1_list[i] + mdmt3_list[i] + mdmt5_list[i] + mdmt7_list[i]) / 4)
        capable_ave = float((mdmt2_list[i] + mdmt4_list[i] + mdmt6_list[i] + mdmt8_list[i]) / 4)
        reliable_ave_list.append(reliable_ave)
        capable_ave_list.append(capable_ave)
        
    # get average values of MDMT
    mdmt_ave_list = []
    for i in range(NUM_PARTICIPANTS * 5):
        this_row_list = [mdmt1_list[i], mdmt2_list[i], mdmt3_list[i], mdmt4_list[i], mdmt5_list[i], mdmt6_list[i], mdmt7_list[i], mdmt8_list[i]]
        mdmt_ave = ave_of_list(this_row_list)
        mdmt_ave_list.append(mdmt_ave)
    
    grouped_auto_list = get_grouped_auto_list(auto_id_list)
    
    # generate new dataframe
    df_dict = {
        'pid': part_id_list,
        'trust_tech': list_times_five(trust_tech_list),
        'play_games': list_times_five(play_games_list),
        'play_music': list_times_five(play_music_list),
        'order': list_times_five(order_list),
        'autonomy': auto_id_list,
        'auto_grouped': grouped_auto_list,
        'mdmt_reliable': mdmt1_list,
        'mdmt_capable': mdmt2_list,
        'mdmt_predictable': mdmt3_list,
        'mdmt_skilled': mdmt4_list,
        'mdmt_someone': mdmt5_list,
        'mdmt_competent': mdmt6_list,
        'mdmt_consistent': mdmt7_list,
        'mdmt_meticulous': mdmt8_list,
        'mdmt_reliable_ave': reliable_ave_list,
        'mdmt_capable_ave': capable_ave_list,
        'mdmt_ave': mdmt_ave_list
    }
    mdmt_df = DataFrame(df_dict)
    
    # write new dataframe to csv file
    dest_path = getcwd() + "\questionnaires\data" + '\\mdmt_preprocessed.csv'
    mdmt_df.to_csv(dest_path, index=False)
    
    mdmt_df = remove_med_auto(mdmt_df)
    # write new dataframe to csv file
    dest_path = getcwd() + "\dataframes" + '\\mdmt.csv'
    mdmt_df.to_csv(dest_path, index=False)
    
    print(" Successfully written pre-processed data to csv file! \n")


##########################################################################################
def preprocess_p_auto():
    
    # get overall dataframe
    raw = get_raw_data()
    demo_df = get_demo_data()
    order_list = demo_df['order'].tolist()
    trust_tech_list = demo_df['trust_tech'].tolist()
    play_games_list = demo_df['play_games'].tolist()
    play_music_list = demo_df['play_music'].tolist()
    
    # get first 2 columns as lists
    part_id_list = raw.iloc[2:NUM_PARTICIPANTS*5+2, 0].tolist()
    for i in range(len(part_id_list)):
        part_id_list[i] = int(sub("P", "", part_id_list[i]))
    alpha_id_list_str = raw.iloc[2:NUM_PARTICIPANTS*5+2, 1].tolist()
    auto_id_list = [round(float(1.0 - float(alpha_id_list_str[i])/5.0), 1) for i in range(len(alpha_id_list_str))]
        
    # get last 2 columns as lists
    p_auto_list_str = raw.iloc[2:NUM_PARTICIPANTS*5+2, 16].tolist()
    p_auto_list = [int(p_auto_list_str[i]) for i in range(len(p_auto_list_str))]
    
    grouped_auto_list = get_grouped_auto_list(auto_id_list)
    
    # generate new dataframe
    df_dict = {
        'pid': part_id_list,
        'trust_tech': list_times_five(trust_tech_list),
        'play_games': list_times_five(play_games_list),
        'play_music': list_times_five(play_music_list),
        'order': list_times_five(order_list),
        'autonomy': auto_id_list,
        'auto_grouped': grouped_auto_list,
        'p_auto': p_auto_list
    }
    p_auto_df = DataFrame(df_dict)
    
    # write new dataframe to csv file
    dest_path = getcwd() + "\questionnaires\data" + '\\p_auto_preprocessed.csv'
    p_auto_df.to_csv(dest_path, index=False)
    
    p_auto_df = remove_med_auto(p_auto_df)
    # write new dataframe to csv file
    dest_path = getcwd() + "\dataframes" + '\\p_auto.csv'
    p_auto_df.to_csv(dest_path, index=False)
    
    print(" Successfully written pre-processed data to csv file! \n")
    
    
##########################################################################################
def preprocess_p_trust():
    
    # get overall dataframe
    raw = get_raw_data()
    demo_df = get_demo_data()
    order_list = demo_df['order'].tolist()
    trust_tech_list = demo_df['trust_tech'].tolist()
    play_games_list = demo_df['play_games'].tolist()
    play_music_list = demo_df['play_music'].tolist()
    
    # get first 2 columns as lists
    part_id_list = raw.iloc[2:NUM_PARTICIPANTS*5+2, 0].tolist()
    for i in range(len(part_id_list)):
        part_id_list[i] = int(sub("P", "", part_id_list[i]))
    alpha_id_list_str = raw.iloc[2:NUM_PARTICIPANTS*5+2, 1].tolist()
    auto_id_list = [round(float(1.0 - float(alpha_id_list_str[i])/5.0), 1) for i in range(len(alpha_id_list_str))]
        
    # get last 2 columns as lists
    p_trust_list_str = raw.iloc[2:NUM_PARTICIPANTS*5+2, 17].tolist()
    p_trust_list = [int(p_trust_list_str[i]) for i in range(len(p_trust_list_str))]
    
    grouped_auto_list = get_grouped_auto_list(auto_id_list)
    
    # generate new dataframe
    df_dict = {
        'pid': part_id_list,
        'trust_tech': list_times_five(trust_tech_list),
        'play_games': list_times_five(play_games_list),
        'play_music': list_times_five(play_music_list),
        'order': list_times_five(order_list),
        'autonomy': auto_id_list,
        'auto_grouped': grouped_auto_list,
        'p_trust': p_trust_list
    }
    p_trust_df = DataFrame(df_dict)
    
    # write new dataframe to csv file
    dest_path = getcwd() + "\questionnaires\data" + '\\p_trust_preprocessed.csv'
    p_trust_df.to_csv(dest_path, index=False)
    
    p_trust_df = remove_med_auto(p_trust_df)
    # write new dataframe to csv file
    dest_path = getcwd() + "\dataframes" + '\\p_trust.csv'
    p_trust_df.to_csv(dest_path, index=False)
    
    print(" Successfully written pre-processed data to csv file! \n")
    

##########################################################################################
def ave_of_list(my_list):
    sum = 0.0
    count = 0
    for n in my_list:
        sum += n
        count += 1
    return sum / count


##########################################################################################
def main():
    
    preprocess_tlx()
    
    preprocess_mdmt()
    
    


    
##########################################################################################
if __name__ == "__main__":
    
    main()
    