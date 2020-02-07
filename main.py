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

#---------Remove comma and turn string into intenger-------
#--------------"700,000" into 700000-------------

def comma_str_to_int(a_str):
  try:
    a_str=re.sub(",", "", a_str)
    a_num=re.sub('[^0-9]', "", a_str)
    a_num=int(a_num)
  except:
    a_num=np.nan
  return a_num
#-----------------If there is a point in string this function
#-------------------turn the string into a float
#----------------------For example: "$23.4" into 23.4

def point_str_to_float(a_str):
  try:
    a_num=re.findall(r"[-+]?\d*\.\d+|\d+", a_str)
    a_num=float(a_num[0])
  except:
    a_num=np.nan
  return a_num

#--------------no regex version---------------
# ---------------turn any string into foat-------------
def anystring_to_float(string):
  newstring ="" 
  my_float=""
  count=0
  for a in string: 
      if a=='.' or (a.isnumeric()) == True: 
          count+= 1
          my_float+=a
      else: 
          newstring+= a 
  print(count) 
  print(newstring) 
  print('data type of {} is now {}'.format(num, type(num))
)
  return float(my_float)

# anystring_to_float(string)


def change_df(df):
  for i in indice_of_columns:
    print(df.columns[i])
    df[df.columns[i]]=df[df.columns[i]].map(lambda row:anystring_to_float(row))
  return df
