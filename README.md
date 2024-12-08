Readme File for Final Project

SETUP OF THE PROJECT:
1.  Clone the Repository; git clone https://github.com/varshankumar/DBMS-Final-Project.git
2.  Run "pip install -r requirements.txt"
3. Change the DDL file path in __init__.py (Copy and paste the entire path of the ddl.sql file and not the Relative Path)
4. Update the username and password of the MYSQL login, in config.py
5. Run the flask server using run.py to create the database and execute DDLs.
6. Run the trigger.sql file from the MYSQL workbench to execute all the triggers.
5. Need to insert Category table data from the MYSQL workbench before executing the front-end.
USE `dbms_finalproject`;

INSERT INTO `dbms_finalproject`.` category` (`category_id`, `name`, `description`) VALUES
('housing', 'Housing', 'Housing-related expenses such as rent, mortgage, etc.'),
('transportation', 'Transportation', 'Expenses related to transportation like car payments, fuel, public transit, etc.'),
('food', 'Food & Groceries', 'Expenses for food, groceries, and dining out.'),
('utilities', 'Utilities', 'Bills for utilities such as electricity, water, internet, etc.'),
('entertainment', 'Entertainment', 'Spending on entertainment such as movies, events, subscriptions, etc.'),
('healthcare', 'Healthcare', 'Medical expenses including insurance, doctor visits, medications, etc.'),
('savings', 'Savings', 'Funds set aside for savings, investments, or emergency funds.'),
('other', 'Other', 'Any other miscellaneous expenses that do not fit in the above categories.');

7. Open index.html from the templates folder to access the front end.
8. Now you are ready to register and use the FINANCIAL TRACKER application.

DIVISION OF WORK:
1.	Sai Pranav Sripathi (SJSU ID: 018188677)
    a.	Worked on implementing backend structure using Python and Flask and implemented API routes for users and accounts.
    b.	Worked on the second round of database testing and modifications using MYSQL.
    c.	Contributed to database design, project proposal, and other documentation.
2.	Prasanna Sai Rohit Durbha (SJSU ID: 018230693)
    a.	Worked on implementing the front-end connection to the APIs using HTML for multiple entities.
    b.	Worked on the first round of testing for the application.
    c.	Contributed to database design, project proposal, and other documentation.
3.	Abhishek Rasikbhai Shekhada (SJSU ID: 017609475)
    a.	Worked on the front-end framework using HTML.
    b.	Worked on final report consolidation and presentation.
    c.	Contributed to database design, project proposal, and other documentation.
4.	Varshan Kumar (SJSU ID: 017099368)
    a.	Worked setting up repository, the goals API route and application front-end code
    b.	Worked on meeting minutes and other documentation for the project.
    c.	Contributed to database design, project proposal, and other documentation.
5.	Kumari Shyama (SJSU ID: 018231512)
    a.	Worked on Database design, creation of the database, and the first round of testing for the database using MYSQL.
    b.	Worked on the implementation of multiple API routes using Python and Flask.
    c.	Contributed to the Project proposal, presentation, and other documentation.