# data.py
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

print("파일명을 입력해주세요: ", end = ' ')
file = f"{input()}"
data=pd.read_csv(file)
m=np.arange(1,13,1)

def print_data():
    print(data)

def print_visual_data():
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
