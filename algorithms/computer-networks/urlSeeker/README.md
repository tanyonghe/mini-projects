# urlSeeker

## What is urlSeeker?
urlSeeker is a parallel web crawler implemented in Python that stores the URL of visited web pages. 
Because using time as a stopping criterion would sometimes cause an error when workers are terminated without warning, 
a smoother stopping criterion has been implemented using the number of processed URLs. 
A user can either set a timer for how long urlSeeker runs or set a limit as to how many URLs should be processed before the crawler terminates.


## Future Enhancements
1)	Filtering URLs to allow only URLs from the same origin.
2)	Track number of uniquely scraped URLs as another stopping criterion.


## Development Environment
```
Microsoft Windows 10 Home Version 10.0.17134 Build 17134
Python 3.6.5
```


## Instructions
1) Run the Python file under default settings.
```
python urlSeeker.py
```

2) If there are user-defined requirements, edit the `User-defined Variables` portion in the Python file.