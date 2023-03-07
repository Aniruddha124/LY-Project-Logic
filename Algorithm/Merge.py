import numpy as np
import pandas as pd

def Merge(start, end, filename):
    merged_df = pd.DataFrame()
    for i in range(start, end):
        df = pd.read_csv("Datasets_Generated/WhiteAddressInfo/Output_" + str(i) + ".csv")
        merged_df = merged_df.append(df, ignore_index=True)
    merged_df.to_csv('./Datasets_Generated/Merged_Datasets/' + str(filename) + '.csv', index=False, header=True)

if __name__ == '__main__':
    # Merge(0, 9, "White_Merged")
    # print("Datasets Merged")
    df_white = pd.read_csv("./Datasets_Generated/Merged_Datasets/White_Merged.csv")
    df_black = pd.read_csv("./Datasets_Generated/Merged_Datasets/Black_Merged.csv")
    df_white['is_Malicious'] = 0
    df_black['is_Malicious'] = 1
    df = df_white.append(df_black, ignore_index=True)
    df.to_csv('./Datasets_Generated/Merged_Datasets/Final_Merged.csv', index=False, header=True)