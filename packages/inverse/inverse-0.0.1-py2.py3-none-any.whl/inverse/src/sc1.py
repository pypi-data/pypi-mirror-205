
#filename:sc1.py
#folder:
import numpy as np
import pandas as pd
arr = np.array([[1, 2, 3], [4, 5, 6]])
def nparray_to_df(array):
    liste = []
    for x in array:
        y = list(x)
        liste.append(y)
    return pd.DataFrame(liste).transpose()
# df = nparray_to_df(arr)
# print(df)
# print(df.columns)
bulk = []
big_bulk = []
treshold = 9
def ekle_bulk(i):
    global big_bulk
    global bulk
    if not i in bulk:
        bulk.append(i)
    if len(bulk) > treshold:
        big_bulk.append(bulk)
        bulk = []
def check1(n=100):
    for i in range(n):
        for j in range(n):
            if j != i :
                ekle_bulk(str(i) + "*" * 20)
                ekle_bulk(j)
check1()
# print(bulk)
print(big_bulk)
def zeros():
    import numpy as np
    # zeros_array = np.zeros((1000, 1000_000), dtype='uint8')
    zeros_array = np.zeros((100, 100), dtype='uint8')
    zeros_array[1][1] = 1
    print(zeros_array)
    print(zeros_array.nbytes)
# zeros()
