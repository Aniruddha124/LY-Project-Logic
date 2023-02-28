import numpy as np
import pandas as pd

def Merge(start, end, filename):
    merged_df = pd.DataFrame()
    for i in range(start, end):
        df = pd.read_csv("Datasets_Generated/AddressInfo/Output_" + str(i) + ".csv")
        merged_df = merged_df.append(df, ignore_index=True)
    merged_df.to_csv('./Datasets_Generated/Merged_Datasets/' + str(filename) + '.csv', index=False, header=True)

if __name__ == '__main__':
    Merge(0, 2, "Output")
    print("Datasets Merged")