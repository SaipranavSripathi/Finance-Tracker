Readme File for Final Project

SETUP OF THE PROJECT:
1.  Run "pip install -r requirements.txt"
2. Change the DDL file path in __init__.py (Copy and paste the entire path of the ddl.sql file and not the Relative Path)
3. Update the username and password of the MYSQL login, in config.py
4. Run the flask server using run.py to create the database and execute DDLs.
5. Run the trigger.sql file from the MYSQL workbench to execute all the triggers.
6. Need to insert Category table data from the MYSQL workbench before executing the front-end.
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
