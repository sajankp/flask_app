Flask Api to Calculate Total Cost

The flask server can be run using the script runserver.sh

the api default path in local is http://127.0.0.1:5000/
Only POST method is used to prevent entry from crawlers or from browser.

There is a validation for the keys in API as 'distance' and 'order_items' are mandatory.
'offer' is optional key and has two types if present, else it is zero by default.
In case of errors related to missing keys the status code 400 is raised with necessary information.

Unrecognized discount type causes 401 with relevant information. 
There is an error in the data (ie negative for product info) there is status code 400.
Distance based slabs are setup using dictionary but max value is 50000m (even if beyond the delivery fee remains the same as in problem statement)


Output is as follows
{'order_total':<amount in paisa>}

 