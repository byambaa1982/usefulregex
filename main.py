import pandas as pd 
import numpy as np 




#--------------no regex version---------------
# ---------------turn any string into foat-------------
def anystring_to_float(string):
  newstring ="" 
  my_float=""
  count=0
  try:
    for a in string: 
        if a=='.' or (a.isnumeric()) == True: 
            count+= 1
            my_float+=a
        else: 
            newstring+= a 
    # print(count) 
    # print(newstring) 
    # print('data type of {} is now {}'.format(num, type(num)))
    return float(my_float)
  except:
    return np.nan


# anystring_to_float(string)


def change_df(df):
  for i in indice_of_columns:
    print(df.columns[i])
    df[df.columns[i]]=df[df.columns[i]].map(lambda row:anystring_to_float(row))
  return df


#--------You should change indice list here: ---------


indice_of_columns=[5,7,8,9]
change_df(df)
