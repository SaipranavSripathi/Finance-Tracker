from sqlalchemy import text
from app import db
import os

def execute_sql_file(app, filepath):
    with app.app_context():
        if os.path.exists(filepath):
            with open(filepath, 'r') as file:
                sql_commands = file.read()
            try:
                for command in sql_commands.split(';'):
                    if command.strip():
                        db.session.execute(text(command))
                db.session.commit()
                print(f"Successfully executed SQL file: {filepath}")
            except Exception as e:
                print(f"Error executing SQL file: {e}")
        else:
            print(f"SQL file not found: {filepath}")

# def execute_triggers(app) :
#     trigger_sql = """
#     CREATE TRIGGER CalculateAggregate
#     AFTER INSERT ON Transaction
#     FOR EACH ROW
#     BEGIN
#         UPDATE Aggregate
#         SET 
#             total_income = (
#                 SELECT COALESCE(SUM(amount), 0)
#                 FROM Transaction
#                 WHERE user_id = NEW.user_id AND amount > 0
#             ),
#             total_expenditure = (
#                 SELECT COALESCE(SUM(amount), 0)
#                 FROM Transaction
#                 WHERE user_id = NEW.user_id AND amount < 0
#             ),
#             generated_at = CURRENT_TIMESTAMP
#         WHERE user_id = NEW.user_id
#     END
#     """
    
#     try:
#         # Make sure to run this inside the app context
#         with app.app_context():
#             # Execute the trigger creation SQL
#             db.session.execute(text(trigger_sql))
#             db.session.commit()  # Commit changes to the database
#             print("Trigger 'CalculateAggregate' created successfully.")
#     except Exception as e:
#         # Rollback the session in case of error
#         with app.app_context():
#             db.session.rollback()
#         print(f"Error executing trigger SQL: {e}")    
