bookutil
========
a command line menu app that gets books from the google book API and creates a library.
features incude:
- create a library based on a search string
- save and load the library to a CSV format file
- group books by publishers and formats and save to CSV
- sort books by price, average rating, ratings count, published date and pages


how to run it
-------------
set up environment:  
`git clone <repo url>`  
`cd bookutil`  
`virtualenv . --no-site-packages`  
`source bin/activate`  
`pip install -r requirements.txt`  

run application:  
`python main_menu.py`  


items to note
-------------
- if a book does not have the attribute being grouped or sorted, it is omitted from the results.
- able to load library from a CSV made by the group by function even if it is under 100 books.

