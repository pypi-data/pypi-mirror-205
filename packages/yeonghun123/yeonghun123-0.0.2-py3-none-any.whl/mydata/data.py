# data.py
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
data=pd.read_csv("C:\\Users\\jyh11\\Desktop\\JYH11224\\workspace\\B_JUN_python\\busan_dust.csv")
m=np.arange(1,13,1)

def print_data():
    print(data)

def print_visual_data():
    result=[]
    for x in m:
        rest=data[str(x)].sum()

        result.append(rest)
    print(data)
    plt.xticks(m)
    plt.xlabel('month')
    plt.ylabel('year')
    plt.title('Number of dust storm days per month in Busan')
    plt.bar(m,result)

    plt.show()
