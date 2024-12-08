from flask import Blueprint, jsonify, current_app, logging, request, session
from app.extensions import db, migrate
from flask_cors import CORS
from sqlalchemy import text

api = Blueprint('api', __name__)

# Enable CORS for all routes
CORS(api)



@api.route('/hello')
def home():
    return jsonify({'message': 'Welcome to the SSP API TEST!'})

@api.route('/register', methods=['POST'])
def add_user():
    """
    Endpoint to add a new user to the database.
    The user_id is auto-generated by the database.
    """
    try:
        # Get JSON data from the request
        data = request.get_json()
        
        # Validate required fields
        if not all(key in data for key in ("name", "email", "password", "birthdate")):
            return jsonify({"error": "Missing required fields (name, email, password, birthdate)."}), 400
        
        # Extract fields from the JSON payload
        # user_id=data["user_id"]
        name = data["name"]
        email = data["email"]
        password = data["password"]
        birthdate = data["birthdate"]
        
        # Construct the SQL query
        insert_query = """
        INSERT INTO User (name, email, password, birthdate) 
        VALUES (:name, :email, :password, :birthdate)
        """
        
        # Execute the query
        with current_app.app_context():
            result = db.session.execute(
                text(insert_query), 
                {
                    "name": name,
                    "email": email,
                    "password": password,
                    "birthdate": birthdate
                }
            )
            db.session.commit()
        return jsonify({"message": "User added successfully!"}), 201
    
    except Exception as e:
        # Rollback in case of an error
        with current_app.app_context():
            db.session.rollback()
        return jsonify({"error": str(e)}), 500


@api.route('/login', methods=['POST'])
def login_user():
    """
    Endpoint to authenticate a user using the database entry and create a session.
    """
    try:
        data = request.get_json()
        
        # Check if required fields are in the request
        if not all(key in data for key in ("email", "password")):
            return jsonify({"error": "Missing required fields (email, password)."}), 400
        
        email = data["email"]
        password = data["password"]
        
        # Fetch user from the database
        select_query = "SELECT * FROM user WHERE email = :email"
        with current_app.app_context():
            result = db.session.execute(text(select_query), {"email": email})
            user = result.fetchone()

            # Check if user exists and if the password matches
            if not user or user[2] != password:
                return jsonify({"error": "Invalid credentials!"}), 401

        # Create a session for the user in the Session table (optional)
        insert_query = "UPDATE Session SET status='ACTIVE' WHERE user_id = :user_id"
        with current_app.app_context():
            db.session.execute(
                text(insert_query),
                {"user_id": user[0], "status": "ACTIVE"}
            )
            db.session.commit()

        # Store user data in the Flask session (or cookies)
        session['user_id'] = user[0]  # Store the user_id
        session['user_name'] = user[1]  # Store the user's name

        # Prepare user data for the response
        user_data = {
            "user_id": user[0],
            "name": user[1],  # Return the user's name
            "email": user[3],
            "birthdate": user[4],
        }

        return jsonify({"message": "Login successful!", "user": user_data}), 200

    except Exception as e:
        # Rollback transaction in case of error
        with current_app.app_context():
            db.session.rollback()
        return jsonify({"error": str(e)}), 500


@api.route('/accounts', methods=["POST"])
def get_accounts():
    """
    Endpoint to fetch all the accounts.
    """
    try:
        # Get JSON data from the request
        data = request.get_json()

        # Validate required fields
        if not (key in data for key in ("user_id")):
            return jsonify({"error": "Missing required field user_id."}), 400
        # Extract fields from the JSON payload
        user_id = data["user_id"]
        print(user_id)
        # Construct the SQL query
        select_query = """
        SELECT * FROM Account WHERE user_id = :user_id
        """
        
        # Execute the query
        with current_app.app_context():
            result = db.session.execute(
                text(select_query), 
                {"user_id": user_id}
            )
        
            # Fetch the row
            accounts = result.fetchall()  # Returns all rows as a tuple or None if no data is found
            print(accounts)
            if not accounts:
                return jsonify({"error": "Accounts not found!"}), 404
           
            db.session.commit()
        
        # Prepare the response
        accounts_data=[]
        for account in accounts :
            account_data={}
            account_data = {
                "account_number": account[0],
                "name": account[1],
                "current_balance": account[2],
                "type": account[3],
                "user_id": account[4],
                "category_id": account[5]
            }
            accounts_data.append(account_data)

        return jsonify({"message": "Accounts fetched!!", "account": accounts_data}), 200

    except Exception as e:
        # Rollback in case of an error
        with current_app.app_context():
            db.session.rollback()
        return jsonify({"error": str(e)}), 500

@api.route('/add_accounts', methods=['POST'])
def add_accounts():
    """
    Endpoint to add new accounts.
    """
    try:
        # Get JSON data from the request
        data = request.get_json()

        # Validate required fields
        if not all(key in data for key in ("user_id","name","type","category_id")):
            return jsonify({"error": "Missing required field user_id/name/type/category_id."}), 400
        # Extract fields from the JSON payload
        user_id = data["user_id"]
        name = data["name"]
        current_balance=data["current_balance"]
        type=data["type"]
        category_id=data["category_id"]

        # Construct the SQL query
        select_query = """
        INSERT INTO Account (name, type, user_id, category_id, current_balance) 
        VALUES (:name, :type, :user_id, :category_id, :current_balance)
        """
        
        # Execute the query
        with current_app.app_context():
            result = db.session.execute(
                text(select_query), 
                {
                    "name": name,
                    "current_balance": current_balance,
                    "type": type,
                    "user_id": user_id,
                    "category_id": category_id
                 }
            )
            db.session.commit()
        return jsonify({"message": "Account added successfully!"}), 201
        
    except Exception as e:
        # Rollback in case of an error
        with current_app.app_context():
            db.session.rollback()
        return jsonify({"error": str(e)}), 500
    

#Method for getting transactions from the DB.    
@api.route('/transaction', methods=['POST'])
def get_transactions():
    """
    Endpoint to fetch all the transactions with optional filters.
    """
    try:
        # Get JSON data from the request
        data = request.get_json()

        # Validate required fields
        if not ("user_id" in data):
            return jsonify({"error": "Missing required field user_id"}), 400

        user_id = data["user_id"]
        date_filter = data.get("date")
        type_filter = data.get("type")
        category_filter = data.get("category")
        status_filter = data.get("status")

        # Construct the SQL query with filters if provided
        select_query = """
        SELECT * FROM Transaction WHERE user_id = :user_id
        """

        filters = {"user_id": user_id}
        if date_filter:
            select_query += " AND date >= :date"
            filters["date"] = date_filter
        if type_filter:
            select_query += " AND type = :type"
            filters["type"] = type_filter
        if category_filter:
            select_query += " AND category_id = :category"
            filters["category"] = category_filter
        if status_filter:
            select_query += " AND status = :status"
            filters["status"] = status_filter

        # Execute the query
        with current_app.app_context():
            result = db.session.execute(
                text(select_query), filters
            )
        
            # Fetch the row
            transactions = result.fetchall()  # Returns all rows as a tuple or None if no data is found
            if not transactions:
                return jsonify({"error": "No transactions found!"}), 404

        # Prepare the response
        transaction_data = [] 
        for transaction in transactions:
            transaction_data.append({
                "transaction_id": transaction[0],
                "amount": transaction[1],
                "type": transaction[2],
                "date": transaction[3],
                "balance": transaction[4],
                "status": transaction[5],
                "user_id": transaction[6],
                "category_id": transaction[7],
                "account_number": transaction[8]
            })

        return jsonify({"message": "Transactions fetched successfully!", "transaction": transaction_data}), 200

    except Exception as e:
        # Rollback in case of an error
        with current_app.app_context():
            db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
# Method for adding transaction to the DB.
@api.route('/add_transaction', methods=['POST'])
def add_transaction():
    try:
        # Get JSON data from the request
        data = request.get_json()
        
        # Validate required fields
        if not all(key in data for key in ("amount","type", "date","status", "user_id", "category_id", "account_number")):
            return jsonify({"error": "Missing required fields (amount,type,date,status,user_id,category_id,account_number)."}), 400
        
        # Extract fields from the JSON payload
        amount=data["amount"]
        type = data["type"]
        date = data["date"]
        status = data["status"]
        user_id = data["user_id"]
        category_id = data["category_id"]
        account_number = data["account_number"]
        
        # Construct the SQL query
        insert_query = """
        INSERT INTO Transaction (amount, type, date, status, user_id, category_id, account_number) 
        VALUES (:amount, :type, :date, :status, :user_id, :category_id, :account_number)
        """
        
        # Execute the query
        with current_app.app_context():
            result = db.session.execute(
                text(insert_query), 
                {
                    "amount": amount,
                    "type": type,
                    "date": date,
                    "status": status,
                    "user_id": user_id,
                    "category_id": category_id,
                    "account_number": account_number
                }
            )
            db.session.commit()
        return jsonify({"message": "Transaction added successfully!", "success": True}), 201
    
    except Exception as e:
        # Rollback in case of an error
        with current_app.app_context():
            db.session.rollback()
        return jsonify({"error": str(e)}), 500

#Method for getting budget from the DB.
#Method for getting budget from the DB.
@api.route('/budget', methods=['POST'])
def get_budget():
    """
    Endpoint to fetch budget details.
    """
    try:
        # Get JSON data from the request
        data = request.get_json()

        # Validate required fields
        if not (key in data for key in ("user_id")):
            return jsonify({"error": "Missing required field (user_id)"}), 400
        # Extract fields from the JSON payload
        user_id = data["user_id"]
        
        # Construct the SQL query
        select_query = """
        SELECT * FROM Budget WHERE user_id = :user_id
        """
        # Execute the query
        with current_app.app_context():
            result = db.session.execute(
                text(select_query), 
                {"user_id": user_id}
            )
        
            # Fetch the row
            budgets = result.fetchall()  # Returns all rows as a tuple or None if no data is found
            if not budgets:
                return jsonify({"error": "User or Category not found!"}), 404
        
        # Prepare the response
        budget_data = [] 
        for budget in budgets:
            budget_data.append({
            "budget_id": budget[0],
            "amount": budget[1],
            "start_date": budget[2],
            "end_date": budget[3],
            "user_id": budget[4],
            "category_id": budget[5]
        })

        return jsonify({"message": "Budget details fetched!!", "budget": budget_data}), 200

    except Exception as e:
        # Rollback in case of an error
        with current_app.app_context():
            db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
# Method for adding budget to the DB.
@api.route('/add_budget', methods=['POST'])
def add_budget():
    try:
        # Get JSON data from the request
        data = request.get_json()
        
        # Validate required fields
        if not all(key in data for key in ("amount","start_date", "end_date", "user_id", "category_id")):
            return jsonify({"error": "Missing required fields (amount,start_date,end_date,user_id,category_id)."}), 400
        
        # Extract fields from the JSON payload
        amount=data["amount"]
        start_date = data["start_date"]
        end_date = data["end_date"]
        user_id = data["user_id"]
        category_id = data["category_id"]
        
        # Construct the SQL query
        insert_query = """
        INSERT INTO Budget (amount, start_date, end_date, user_id, category_id) 
        VALUES (:amount, :start_date, :end_date, :user_id, :category_id)
        """
        
        # Execute the query
        with current_app.app_context():
            result = db.session.execute(
                text(insert_query), 
                {
                    "amount": amount,
                    "start_date": start_date,
                    "end_date": end_date,
                    "user_id": user_id,
                    "category_id": category_id
                }
            )
            db.session.commit()
        return jsonify({"message": "Budget set successfully!"}), 201
    
    except Exception as e:
        # Rollback in case of an error
        with current_app.app_context():
            db.session.rollback()
        return jsonify({"error": str(e)}), 500

#Method for getting category from the DB.    
@api.route('/category')
def get_category():
    """
    Endpoint to fetch category details.
    """
    try:
        # Get JSON data from the request
        data = request.get_json()

        # Validate required fields
        if not all(key in data for key in ("category_id")):
            return jsonify({"error": "Missing required field category_id"}), 400
        # Extract fields from the JSON payload
        category_id = data["category_id"]
        
        # Construct the SQL query
        select_query = """
        SELECT * FROM Category WHERE category_id = :category_id
        """
        # Execute the query
        with current_app.app_context():
            result = db.session.execute(
                text(select_query), 
                {"category_id": category_id}
            )
        
            # Fetch the row
            category = result.fetchall()  # Returns all rows as a tuple or None if no data is found
            if not category:
                return jsonify({"error": "Category not found!"}), 404
        
        # Prepare the response
        category_data = [] 
        for category in category:
            category_data.append({
            "category_id": category[0],
            "name": category[1],
            "description": category[2]
        })

        return jsonify({"message": "Category details fetched!!", "category": category_data}), 200

    except Exception as e:
        # Rollback in case of an error
        with current_app.app_context():
            db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
# Method for adding category to the DB.
@api.route('/add_category', methods=['POST'])
def add_category():
    try:
        # Get JSON data from the request
        data = request.get_json()
        
        # Validate required fields
        if not all(key in data for key in ("category_id","name", "description")):
            return jsonify({"error": "Missing required fields (category_id,name,description)."}), 400
        
        # Extract fields from the JSON payload
        category_id=data["category_id"]
        name = data["name"]
        description = data["description"]
        
        # Construct the SQL query
        insert_query = """
        INSERT INTO Budget (category_id, name, description) 
        VALUES (:category_id, :name, :description)
        """
        
        # Execute the query
        with current_app.app_context():
            result = db.session.execute(
                text(insert_query), 
                {
                    "category_id": category_id,
                    "name": name,
                    "desscription": description
                }
            )
            db.session.commit()
        return jsonify({"message": "Category added successfully!"}), 201
    
    except Exception as e:
        # Rollback in case of an error
        with current_app.app_context():
            db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
#Method for getting goal from the DB.
@api.route('/goal', methods=['POST'])
def get_goal():
    """
    Endpoint to fetch goal details.
    """
    try:
        # Get JSON data from the request
        data = request.get_json()

        # Validate required fields
        if not (key in data for key in ("user_id")):
            return jsonify({"error": "Missing required field user_id"}), 400
        # Extract fields from the JSON payload
        user_id = data["user_id"]


        select_query = """
        SELECT * FROM Goal WHERE user_id = :user_id
        """
        # Execute the query
        with current_app.app_context():
            result = db.session.execute(
                text(select_query), 
                {"user_id": user_id}
            )


            goal = result.fetchall()  # Returns all rows as a tuple or None if no data is found
            if not goal:
                return jsonify({"error": "User not found!"}), 404


        goal_data = [] 
        for goal in goal:
            goal_data.append({
            "goal_id": goal[0],
            "name": goal[1],
            "target": goal[2],
            "deadline": goal[3],
            "user_id": goal[4]
        })

        return jsonify({"message": "Goal details fetched!!", "goal": goal_data}), 200

    except Exception as e:
        # Rollback in case of an error
        with current_app.app_context():
            db.session.rollback()
        return jsonify({"error": str(e)}), 500


# Method for adding goal to the DB.
@api.route('/add_goal', methods=['POST'])
def add_goal():
    try:
        # Get JSON data from the request
        data = request.get_json()
        
        # Validate required fields
        if not all(key in data for key in ("name","target", "deadline", "user_id")):
            return jsonify({"error": "Missing required fields (name,target,deadline,user_id)."}), 400
        
        # Extract fields from the JSON payload
        name=data["name"]
        target = data["target"]
        deadline = data["deadline"]
        user_id = data["user_id"]
        
        # Construct the SQL query
        insert_query = """
        INSERT INTO Goal (name, target, deadline, user_id) 
        VALUES (:name, :target, :deadline, :user_id)
        """       
        # Execute the query
        with current_app.app_context():
            result = db.session.execute(
                text(insert_query), 
                {
                    "name": name,
                    "target": target,
                    "deadline": deadline,
                    "user_id": user_id
                }
            )
            db.session.commit()
        return jsonify({"message": "Goal set successfully!"}), 201
    
    except Exception as e:
        # Rollback in case of an error
        with current_app.app_context():
            db.session.rollback()
        return jsonify({"error": str(e)}), 500
    

#Method for getting aggregate from the DB.    
@api.route('/aggregate', methods=['POST'])
def get_aggregate():
    """
    Endpoint to fetch aggregate transaction details.
    """
    try:
        # Get JSON data from the request
        data = request.get_json()
        user_id = data.get("user_id")
        print(user_id)

        # Validate required fields
        if not (key in data for key in ("user_id")):
            return jsonify({"error": "Missing required field user_id"}), 400
        # Extract fields from the JSON payload
        user_id = data["user_id"]
        
        # Construct the SQL query
        select_query = """
        SELECT * FROM Aggregate WHERE user_id = :user_id
        """
        # Execute the query
        with current_app.app_context():
            result = db.session.execute(
                text(select_query), 
                {"user_id": user_id}
            )
        
            # Fetch the row
            aggregate = result.fetchall()  # Returns all rows as a tuple or None if no data is found
            if not aggregate:
                return jsonify({"error": "User not found!"}), 404
        
        # Prepare the response
        aggregate_data = [] 
        for aggregate in aggregate:
            aggregate_data.append({
            "aggregate_id": aggregate[0],
            "total_income": aggregate[1],
            "total_expenditure": aggregate[2],
            "generated_at": aggregate[3],
            "user_id": aggregate[4]
        })

        return jsonify({"message": "Aggregate details fetched!!", "aggregate": aggregate_data}), 200

    except Exception as e:
        # Rollback in case of an error
        with current_app.app_context():
            db.session.rollback()
        return jsonify({"error": str(e)}), 500

#Method for getting recurring payment from the DB.    
@api.route('/recurring_payment')
def get_recurring_payment():
    """
    Endpoint to fetch recurring_payment details.
    """
    try:
        # Get JSON data from the request
        data = request.get_json()

        # Validate required fields
        if not all(key in data for key in ("user_id", "acount_number")):
            return jsonify({"error": "Missing required field (user_id, account_number)"}), 400
        # Extract fields from the JSON payload
        user_id = data["user_id"]
        account_number = data["account_number"]
        
        # Construct the SQL query
        select_query = """
        SELECT * FROM Recurring_payment WHERE user_id = :user_id and account_number = :account_number
        """
        # Execute the query
        with current_app.app_context():
            result = db.session.execute(
                text(select_query), 
                {"user_id": user_id, "account_number": account_number}
            )
        
            # Fetch the row
            recurring_payment = result.fetchall()  # Returns all rows as a tuple or None if no data is found
            if not recurring_payment:
                return jsonify({"error": "User not found!"}), 404
        
        # Prepare the response
        recurring_payment_data = [] 
        for recurring_payment in recurring_payment:
            recurring_payment_data.append({
            "payment_id": recurring_payment[0],
            "next_due_payment": recurring_payment[1],
            "amount_paid": recurring_payment[2],
            "frequency": recurring_payment[3],
            "next_due_payment_date": recurring_payment[4],
            "user_id": recurring_payment[5],
            "account_number": recurring_payment[6]
        })

        return jsonify({"message": "Recurring payment details fetched!!", "recurring_payment": recurring_payment_data}), 200

    except Exception as e:
        # Rollback in case of an error
        with current_app.app_context():
            db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
# Method for adding recurring payment to the DB.
@api.route('/add_recurring_payment', methods=['POST'])
def add_recurring_payment():
    try:
        # Get JSON data from the request
        data = request.get_json()
        
        # Validate required fields
        if not all(key in data for key in ("next_due_payment","amount_paid", "frequency", "next_due_payment_date", "user_id", "account_number")):
            return jsonify({"error": "Missing required fields (next_due_payment,amount_paid,frequency,next_due_payment_date,user_id,account_number)."}), 400
        
        # Extract fields from the JSON payload
        next_due_payment=data["next_due_payment"]
        amount_paid = data["amount_paid"]
        frequency = data["frequency"]
        next_due_payment_date = data["next_due_payment_date"]
        user_id = data["user_id"]
        account_number = data["account_number"]
        
        # Construct the SQL query
        insert_query = """
        INSERT INTO Recurring_payment (next_due_payment, amount_paid, frequency, next_due_payment_date, user_id, account_number) 
        VALUES (:next_due_payment, :amount_paid, :frequency, :next_due_payment_date, :user_id, :account_number)
        """       
        # Execute the query
        with current_app.app_context():
            result = db.session.execute(
                text(insert_query), 
                {
                    "next_due_payment": next_due_payment,
                    "amount_paid": amount_paid,
                    "frequency": frequency,
                    "next_due_payment_date": next_due_payment_date,
                    "user_id": user_id,
                    "account_number": account_number
                }
            )
            db.session.commit()
        return jsonify({"message": "Recurring payment set successfully!"}), 201
    
    except Exception as e:
        # Rollback in case of an error
        with current_app.app_context():
            db.session.rollback() 
        return jsonify({"error": str(e)}), 500


#Method for getting loan from the DB.    
@api.route('/loan', methods=['POST'])
def get_loan():
    """
    Endpoint to fetch loan details with optional filters for type and date range.
    """
    try:
        # Get JSON data from the request
        data = request.get_json()

        # Validate required fields
        if "user_id" not in data:
            return jsonify({"error": "Missing required field (user_id)"}), 400

        # Extract fields from the JSON payload
        user_id = data["user_id"]
        loan_type = data.get("loan_type")  # Optional filter
        start_date = data.get("start_date")  # Optional filter

        # Construct the SQL query
        select_query = """
        SELECT * FROM Loan WHERE user_id = :user_id
        """
        params = {"user_id": user_id}

        if loan_type:
            select_query += " AND loan_type = :loan_type"
            params["loan_type"] = loan_type

        if start_date:
            select_query += " AND start_date >= :start_date"
            params["start_date"] = start_date

        # Execute the query
        with current_app.app_context():
            result = db.session.execute(text(select_query), params)

            # Fetch the rows
            loan = result.fetchall()
            if not loan:
                return jsonify({"error": "No loans found!"}), 404

        # Prepare the response
        loan_data = []
        for loan in loan:
            loan_data.append({
                "loan_id": loan[0],
                "loan_type": loan[1],
                "amount": loan[2],
                "outstanding_amount": loan[3],
                "interest": loan[4],
                "start_date": loan[5],
                "user_id": loan[6]
            })

        return jsonify({"message": "Loan details fetched!", "loan": loan_data}), 200

    except Exception as e:
        # Rollback in case of an error
        with current_app.app_context():
            db.session.rollback()
        return jsonify({"error": str(e)}), 500

    
# Method for adding loan to the DB.
@api.route('/add_loan', methods=['POST'])
def add_loan():
    try:
        # Get JSON data from the request
        data = request.get_json()
        
        # Validate required fields
        if not all(key in data for key in ("loan_type", "amount", "outstanding_amount","interest", "start_date", "user_id")):
            return jsonify({"error": "Missing required fields (loan_type,amount,outstanding_amount,interest,start_date,user_id)."}), 400
        
        # Extract fields from the JSON payload
        loan_type = data["loan_type"]
        amount = data["amount"]
        outstanding_amount = data["outstanding_amount"]
        interest = data["interest"]
        start_date = data["start_date"]
        user_id = data["user_id"]
        
        # Construct the SQL query
        insert_query = """
        INSERT INTO loan (loan_type, amount, outstanding_amount, interest, start_date, user_id) 
        VALUES (:loan_type, :amount, :outstanding_amount, :interest, :start_date, :user_id)
        """       
        # Execute the query
        with current_app.app_context():
            result = db.session.execute(
                text(insert_query), 
                {
                    "loan_type": loan_type,
                    "amount": amount,
                    "outstanding_amount": outstanding_amount,
                    "interest": interest,
                    "start_date": start_date,
                    "user_id": user_id,
                }
            )
            print('SSP')
            db.session.commit()
        return jsonify({"message": "Loan set successfully!"}), 201
    
    except Exception as e:
        # Rollback in case of an error
        with current_app.app_context():
            db.session.rollback() 
        return jsonify({"error": str(e)}), 500

#Method for getting investment from the DB.    
#Method for getting investment from the DB.    
@api.route('/investment', methods=['POST'])
def get_investment():
    """
    Endpoint to fetch investment details.
    """
    try:
        # Get JSON data from the request
        data = request.get_json()

        # Validate required fields
        if not (key in data for key in ("user_id")):
            return jsonify({"error": "Missing required field (user_id)"}), 400
        # Extract fields from the JSON payload
        user_id = data["user_id"]
        
        # Construct the SQL query
        select_query = """
        SELECT inv.*, invt.type AS investment_type
        FROM investment inv LEFT JOIN investment_type invt 
        ON inv.user_id = invt.user_id AND inv.account_number = invt.account_number AND inv.name = invt.name
        WHERE inv.user_id = :user_id
        """
        # Execute the query
        with current_app.app_context():
            result = db.session.execute(
                text(select_query), 
                {"user_id": user_id}
            )
        
            # Fetch the row
            investment = result.fetchall()  # Returns all rows as a tuple or None if no data is found
            if not investment:
                return jsonify({"error": "User not found!"}), 404
        
        # Prepare the response
        investment_data = [] 
        for investment in investment:
            investment_data.append({
            "investment_id": investment[0],
            "name": investment[1],
            "user_id": investment[2],
            "account_number": investment[3],
            "investment_type": investment[4]
        })

        return jsonify({"message": "Investment details fetched!!", "investment": investment_data}), 200

    except Exception as e:
        # Rollback in case of an error
        with current_app.app_context():
            db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
# Method for adding investment to the DB.
@api.route('/add_investment', methods=['POST'])
def add_investment():
    try:
        # Get JSON data from the request
        data = request.get_json()
        
        # Validate required fields
        if not all(key in data for key in ("name", "user_id", "account_number", "type")):
            return jsonify({"error": "Missing required fields (name,user_id,account_number,type)."}), 400
        
        # Extract fields from the JSON payload
        name = data["name"]
        user_id = data["user_id"]
        account_number = data["account_number"]
        type = data["type"]
        
        # Construct the SQL query
        insert_query = """
        INSERT INTO Investment (name, user_id, account_number) 
        VALUES (:name, :user_id, :account_number)
        """       
        insert_investment_type_query = """
        INSERT INTO investment_type (user_id, account_number, name, type) 
        VALUES (:user_id, :account_number, :name, :type)
        """
        # Execute the query
        with current_app.app_context():
            result = db.session.execute(
                text(insert_query), 
                {
                    "name": name,
                    "user_id": user_id,
                    "account_number": account_number
                }
            )
            type_result=db.session.execute(
                text(insert_investment_type_query),
                {
                    "user_id": user_id,
                    "account_number": account_number,
                    "name": name,
                    "type": type
                }
            )
            db.session.commit()
        return jsonify({"message": "Investment added successfully!", "success":True}), 201
    
    except Exception as e:
        # Rollback in case of an error
        with current_app.app_context():
            db.session.rollback() 
        return jsonify({"error": str(e)}), 500

#Method for getting session from the DB.    
@api.route('/session')
def get_session():
    """
    Endpoint to fetch session details.
    """
    try:
        # Get JSON data from the request
        data = request.get_json()

        # Validate required fields
        if not all(key in data for key in ("user_id")):
            return jsonify({"error": "Missing required field user_id"}), 400
        # Extract fields from the JSON payload
        user_id = data["user_id"]
        
        # Construct the SQL query
        select_query = """
        SELECT * FROM Session WHERE user_id = :user_id and status = 'ACTIVE'
        """
        # Execute the query
        with current_app.app_context():
            result = db.session.execute(
                text(select_query), 
                {"user_id": user_id}
            )
        
            # Fetch the row
            session = result.fetchall()  # Returns all rows as a tuple or None if no data is found
            if not session:
                return jsonify({"error": "User not found!"}), 404
        
        # Prepare the response
        session_data = [] 
        for session in session:
            session_data.append({
            "user_id": session[0],
            "status": session[1]
        })

        return jsonify({"message": "Session type details fetched!!", "session": session_data}), 200

    except Exception as e:
        # Rollback in case of an error
        with current_app.app_context():
            db.session.rollback()
        return jsonify({"error": str(e)}), 500
    
# Method for adding session to the DB.
@api.route('/add_session', methods=['POST'])
def add_session():
    try:
        # Get JSON data from the request
        data = request.get_json()
        
        # Validate required fields
        if not all(key in data for key in ("user_id", "status")):
            return jsonify({"error": "Missing required fields (user_id,status)."}), 400
        
        # Extract fields from the JSON payload
        user_id = data["user_id"]
        status = data["status"]
        
        # Construct the SQL query
        insert_query = """
        UPDATE Session SET status='ACTIVE' WHERE user_id = :user_id
        """       
        # Execute the query
        with current_app.app_context():
            result = db.session.execute(
                text(insert_query), 
                {
                    "user_id": user_id,
                    "status": status
                }
            )
            db.session.commit()
        return jsonify({"message": "Session added successfully!"}), 201
    
    except Exception as e:
        # Rollback in case of an error
        with current_app.app_context():
            db.session.rollback() 
        return jsonify({"error": str(e)}), 500
    

@api.route('/logout', methods=['POST'])
def logout_user():
    """
    Endpoint to authenticate a user using the database entry.
    """
    # print("data")
    try:
        # Get JSON data from the request
        data = request.get_json()


        # Validate required fields
        if not (key in data for key in ("user_id")):
            return jsonify({"error": "Missing required fields (user_id)."}), 400
        # Extract fields from the JSON payload
        user_id = data["user_id"]
        
        # Construct the SQL query
        select_query = """
        UPDATE Session SET status='INACTIVE' WHERE user_id = :user_id
        """
        
        # Execute the query
        with current_app.app_context():
            result = db.session.execute(
                text(select_query), 
                {"user_id": user_id}
            )
            # Commit is unnecessary for SELECT queries, but it won't hurt here
            db.session.commit()
        
        return jsonify({"message": "Logout successful!"}), 200

    except Exception as e:
        # Rollback in case of an error
        with current_app.app_context():
            db.session.rollback()
        return jsonify({"error": str(e)}), 500
        