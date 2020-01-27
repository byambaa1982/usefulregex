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
