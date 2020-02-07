### Data engineering using regex

All code is here:
https://github.com/byambaa1982/usefulregex/blob/master/main.py

If you want to fork the project on github and git clone your fork, e.g.:

    git clone https://github.com/<username>/usfulregex.git
    
As a data scientist, I wasted a lot of time cleaning data, especially for dirty data like the following one.  

Raw data 

![Data](/images/data_pic.png)

Cleaned data

![Data](/images/data_pic2.png)

Problem is that we cannot use following codes because of symbols like '--' or '-' 

	df['DataFrame Column'] = pd.to_numeric(df['DataFrame Column'])

	or 

	df['DataFrame Column'] = df['DataFrame Column'].astype(int)

Let's take a look at one of following cells.

	print(df['Temperature'][0])
	print(df['Apparent temperature'][0])
	print(df['Distance'][0])

Results:
	
	59.55   
	59.55
	1200M


The first two looks like floats,but it will give us 'str' not 'float'.

	print(type(df['Temperature'][0]))
	print(type(df['Apparent temperature'][0]))
	print(type(df['Distance'][0]))

Results:

	<class 'str'>
	<class 'str'>
	<class 'str'>


Befor going further, start simple

    string ='3ad.23'
    
Let's clean this string. '3ad.23' is not digit. 


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

	anystring_to_float(string)

String might be like that "--". Then the function make it into numpy null value. 

Now we can use it for pandas Dataframe. 

	def change_df(df):
	  for i in indice_of_columns:
	    print(df.columns[i])
	    df[df.columns[i]]=df[df.columns[i]].map(lambda row:anystring_to_float(row))
	  return df

Here indice_of_columns is the indice of columns we want to change. In our case, it is 

	indice_of_columns=[5,7,8,9]

Finally, we can run the function 'change_df' and get result. 
Let's check them:

	print(type(df['Temperature'][0]))
	print(type(df['Apparent temperature'][0]))
	print(type(df['Distance'][0]))

New result: 

	<class 'float'>
	<class 'float'>
	<class 'float'>

That simple!


Please connect me in linkedin: 
	https://www.linkedin.com/in/byamba-enkhbat-026722162/
	
	
Hire me here:
	www.fiverr.com/coderjs
