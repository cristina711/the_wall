from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
app = Flask(__name__)
mysql = MySQLConnector(app,'dojowall')
app.secret_key = 'KeepItSecretKeepItSafe'

@app.route('/')
def index():
    
    return render_template('dojowall.html')

@app.route('/process', methods=['POST'])
def process():
    

    if len(request.form['first_name']) < 2:
        flash("Name have to be more than 2 letters!")
    elif  len(request.form['last_name']) < 2:
        flash("Name have to be more than 2 letters!")
    elif  len(request.form['email']) < 2:
        flash("email is invalid!")
    elif  len(request.form['password']) < 8:
        flash("password should be at least 8 characters!")
    elif request.form['confirmation_password'] != request.form['password']:
        flash("Unmatched password!")
    else:
        flash("Success! Your registration is confirmed")
        
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (:first_name, :last_name, :email, :password)"
        # hashed_password = sdlfkmasldkf(request.form['password'])

        data = {
        
             'first_name': request.form['first_name'],
             'last_name': request.form['last_name'],
             'email': request.form['email'],
             'password': request.form['password'],
             
        }
        mysql.query_db(query, data)

        return redirect('/login')

    

@app.route('/login', methods=['get'])
def login():

    return render_template('login.html')
    


@app.route('/success', methods=['POST'])
def success():
    email = request.form['email']
    password = request.form['password']

    query = "SELECT * FROM users WHERE email = :email AND password = :password"

    data = {
        'email': email,
        'password': password
    }
    user = mysql.query_db(query,data)
    
    if user:
        session['id'] = user[0]['id']
        
        return redirect('/wall')
    
    else:
        flash("Unmatched password!")
        return redirect('/wall')

    # query = "SELECT * FROM "                           
    # friends = mysql.query_db(query)



@app.route('/wall', methods=['get'])
def wall():
    message_query = """SELECT users.first_name, users.last_name, messages.message, messages.created_at, messages.id 
    FROM users JOIN messages ON users.id = messages.user_id"""
                          
    messages = mysql.query_db(message_query)    

    comments_query = """SELECT users.first_name, users.last_name, comments.comment, comments.created_at, comments.message_id 
    FROM users JOIN comments ON users.id = comments.user_id"""
                          
    comments = mysql.query_db(comments_query)    
    return render_template('wall.html',all_messages=messages, all_comments= comments)

@app.route('/add_message', methods=['POST'])
def add_message():
    query = "INSERT INTO messages (message, created_at, updated_at, user_id) VALUES (:message, NOW(), NOW(), :user_id)"
    data = {
        'message': request.form['message'],
        'user_id': session['id']
    }
    mysql.query_db(query,data)
    return redirect('/wall')

# @app.route('/show_comment', methods=['get'])
# def show_comment():
#     query = """SELECT users.first_name, users.last_name, comments.comment, comments.created_at, messages.id 
#     FROM users JOIN comments ON users.id = comments.user_id"""
                          
#     comments = mysql.query_db(query)       
#     return render_template('wall.html',all_messages=comments)

@app.route('/add_comment', methods=['POST'])
def add_comment():
    query = "INSERT INTO comments (comment, created_at, updated_at,message_id, user_id) VALUES (:comment, NOW(), NOW(),:message_id, :user_id)"
    data = {
        'comment': request.form['comment'],
        'message_id' :request.form['message_id'],

        'user_id': session['id'],
    }
    mysql.query_db(query,data)
    return redirect('/wall')
app.run(debug=True)


