### Data engineering using regex

All code is here:
https://github.com/byambaa1982/usefulregex/blob/master/main.py

If you want to fork the project on github and git clone your fork, e.g.:

    git clone https://github.com/<username>/usfulregex.git
    
One of my customer want me to clean his data. But his data is very dirty. 

![Data](/images/data_pic.png)
Befor going further, start simple
    test=['23','byamba','df23','(312)-567-11','nan','1000M', 23,'--', np.nan]
    
Let's clean this list. '23' is not digit. Also, I want to turn '(312)-567-11' into 3125670011.
Regex can do this.
    re.sub('[^0-9,]', "", test[i])
   
www.fiverr.com/coderjs
