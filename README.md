### Data engineering using regex

All code is here:
https://github.com/byambaa1982/usefulregex/blob/master/main.py

If you want to fork the project on github and git clone your fork, e.g.:

    git clone https://github.com/<username>/usfulregex.git
    
As a data scientist, I wasted a lot of time cleaning data, especially for dirty data like the following one.  

![Data](/images/data_pic.png)

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

    test=['23','byamba','df23','(312)-567-11','nan','1000M', 23,'--', np.nan]
    
Let's clean this list. '23' is not digit. Also, I want to turn '(312)-567-11' into 3125670011.
Regex can do this.

    re.sub('[^0-9,]', "", test[i])

Please connect me in linkedin: 
	https://www.linkedin.com/in/byamba-enkhbat-026722162/
	
	
Hire me here:
	www.fiverr.com/coderjs
