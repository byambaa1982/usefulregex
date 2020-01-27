import regex as re
#--------string list--------------------
test=['23','byamba','df23','@12-435-(323)','nan','1000M', 23,'--', np.nan]


#------ Pick only numbers---------
def only_number(my_list):
  result=[]
  for i in range(len(test)):
    try:
    	#--- use regex here--------------
      result.append(re.sub('[^0-9,]', "", test[i]))
    except:
      result.append(test[i])
  return result

#------ String to numberic---------
  def to_numberic(my_list):
  my_list=only_number(my_list)
  to_numbers=[]
  for i in range(len(my_list)):
    try:
      # print(my_list[i])
      to_numbers.append(float(my_list[i]))
    except:
      to_numbers.append(np.nan)
  return to_numbers

def str_to_float(a_str):
  try:
    a_num=float(re.sub('[^0-9,]', "", a_str))
  except:
    a_num=np.nan
  return a_num

def change_df(df):
  for i in range(0,df.shape[1]):
    print(df.columns[i])
    df[str(df.columns[i])+'new']=df[str(df.columns[i])].map(lambda row:str_to_float(row))
  return df