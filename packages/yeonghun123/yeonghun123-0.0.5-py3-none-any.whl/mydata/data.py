# data.py
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def print_data():
    print("파일명을 입력해주세요: ", end = ' ')
    file = f"{input()}"
    data=pd.read_csv(file)
    m=np.arange(1,13,1)
    print(data)

def print_visual_data():
    print("파일명을 입력해주세요: ", end = ' ')
    file = f"{input()}"
    data=pd.read_csv(file)
    m=np.arange(1,13,1)
    result=[]
    for x in m:
        rest=data[str(x)].sum()

        result.append(rest)
    plt.xticks(m)
    plt.xlabel('month')
    plt.ylabel('year')
    plt.title('Number of dust storm days per month in Busan')
    plt.bar(m,result)

    plt.show()
