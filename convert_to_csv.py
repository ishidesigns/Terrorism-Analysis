"""
Hadoop, Spark, Data Bricks- tools used to handle big data

"""
#converting excel file to csv file
import pandas as pd

def main():
    print("Welcome to Project Season 3")
    
    dataset = "globalterrorismdb_0919dist.xlsx"
    df = pd.read_excel(dataset)
    type(df)
    df.ndim
    df.columns.tolist()
    
    selected_columns = [1,2,3,7,8,9,10,11,12,13,14,28,29,34,35,40,41,58,81,82,98,105,106]
    df = pd.read_excel(dataset, usecols=selected_columns)
    df.to_csv('global_terror1.csv', header=True, index = False)
    
    my_list=df.columns.tolist()
    my_list
    print("Thanks for using my project")


if __name__ == '__main__':
    main()
    
