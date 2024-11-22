# Receipt Processor

The challenge is to build a webservice that has the API endpoints as specified:

1. POST --> /receipts/process: Body: JSON payload, Output: JSON containing id for receipt.
2. GET --> /receipts/{id}/points: Body: N/A, Output: JSON containing the number of points.

## Workflow

I used Python and the Django framework as the technologies for the assignment. 

Per the instructions, since it was sufficent to store the data in memory, 
no models were built and instead, data is being persisted in files in the 
data directory. 

Per the instructions, since Go was not used, a Dockerfile is provided 
with the configurations needed to run the webservice.

Here's a command to build the docker image:

```docker build -t receipt_processor .```

Here's a command to run the docker image:

```docker run -it -p 8000:8000 receipt_processor```

## Design Considerations

Per Django, I created two routes in the views file. 

In order to calculate the points, I created a series of utility classes in points.py.

In addition, to interact with the database, I created a `DBStore` class in db.py which has 
methods to write and read from csv files in the data directory. 

## Unit Test

To do some testing of the application, it will be important to set the 
environment variable `UNIT_TEST`:

```EXPORT UNIT_TEST=True```

This variable will determine which 
data file to write to or read from to allow for separation of data. 

## Closing 

In closing, I really enjoyed working on this assignment. Thank you for giving me the opportunity to work
on this exercise. 
