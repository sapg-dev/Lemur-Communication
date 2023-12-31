from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from pusher import Pusher
from dotenv import load_dotenv
from datetime import datetime
from db import db, Message, Company, User, ChatRoom
from flask import flash
import hashlib
import random
import string
import uuid
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from flask_login import LoginManager
from flask_login import login_required
from flask_login import current_user
from werkzeug.security import check_password_hash
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
from flask import send_from_directory
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os
import random
import string

from cryptography.fernet import Fernet, InvalidToken


app = Flask(__name__)

load_dotenv(dotenv_path='.env')
app.secret_key = 'some_secret_key'  # Set a secret key for session management
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db'  # Add your database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
login_manager = LoginManager()
login_manager.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


db.init_app(app)  # Initialize the db with the Flask app
pusher = Pusher(
    app_id='1701887',
    key='d65c1eee46cdcd199bc6',
    secret='f7d4323687a227294a2a',
    cluster='eu',
    ssl=True
)

class TerminalChat():
    users = {
        "pacifictrout": "App123",
        "dingleberry": "App123",
      
    }
    

    @staticmethod
    def login(username, password):
        if TerminalChat.users.get(username) == password:
            session['user'] = username
            return True
        return False



@app.route('/', methods=['GET', 'POST'])
def index():
    
    if(current_user.is_authenticated):
        logout_user()

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):

            user_primary_key = User.query.filter_by(username=username).first().id
            company_id = User.query.filter_by(username=username).first().company_id
            company_password = User.query.filter_by(username=username).first().id
            session['user'] = username
            session['company_id'] = company_id
            session['company_password'] = company_password
            login_user(user) 
            print(user.is_authenticated)
        
            return redirect(url_for('select_chatroom', username=current_user.username))

        else:
            flash('Invalid username or password')

    return render_template('login.html')
@app.route('/user/<username>/select-chatroom', methods=['GET', 'POST'])
@login_required
def select_chatroom(username):
    # No need to fetch the user again if using Flask-Login, current_user should be used directly
    company_id = current_user.company_id

    if request.method == 'POST':
        chatroom_name = request.form.get('chatroom_name')
        print(chatroom_name)
        action = request.form.get('action')

        if action == "Join Chatroom": # Joining existing chatroom logic
            chatroom = ChatRoom.query.filter_by(name=chatroom_name, company_id=company_id).first()
            if chatroom:
                print("aosulute retard")
                # Your logic when the chatroom exists (like using Pusher)
                session['current_chatroom'] = chatroom.name
                session['chatroom_id'] = chatroom.id
                pusher.trigger(chatroom_name, 'user_joined', {'message': f"{session['user']} joined the chat"})
                # Triggering Pusher event or any other action
                return redirect(url_for('chat', chatroom_id=chatroom.id))  # Redirect to chat view
            else:
                flash('Chatroom does not exist.', 'danger')

        elif action == "Create Room":
            print("djlsnfvousdvidnsivndsundsfcdsnisdfdsijdnijncsdncidsnivdsjvdnn")
            chatroom_name = request.form.get('new_chatroom_name')
            print(chatroom_name)
            new_chatroom = ChatRoom(name=chatroom_name, company_id=company_id)
            db.session.add(new_chatroom)
            try:
                db.session.commit()
                flash('New chat room created!', 'success')
                session['current_chatroom'] = new_chatroom.name
                
               
                # Redirect to the chat view or refresh the page to show the new chatroom
                return redirect(url_for('select_chatroom'))
            except Exception as e:
                db.session.rollback()
                flash('Error adding chat room: ' + str(e), 'danger')
        else:
            flash('Chatroom name is required.', 'warning')

    chatrooms = ChatRoom.query.filter_by(company_id=company_id).all()
    return render_template('chatroom.html', chatrooms=chatrooms)

@app.route('/chat')
def chat():
    print()
    
    new_room = session.get('current_chatroom')
    
    # Fetch the last N messages from the database
    # Adjust the number of messages as needed
    num_messages_to_load = 1000  # For example, load the last 50 messages
    messages = Message.query \
        .filter_by(chatroom_id=session['chatroom_id']) \
        .order_by(Message.timestamp.asc()) \
        .limit(num_messages_to_load) \
        .all()
    print(messages)
    # Format messages for display
    formatted_messages = [
        {
            'user': message.username,
            'message': message.message,
            'timestamp': message.timestamp.strftime("%A, %H:%M")
        }
        for message in messages
    ]
    
    # Pass the messages to the template
    return render_template('chat.html', username=session['user'], messages=formatted_messages)


@app.route('/send_message', methods=['POST'])
def send_message():
    username = session.get('user', 'Anonymous')
    print(username)
    message_content = f"{username}: {request.form.get('message')}"
    timestamp = datetime.utcnow()
    chatroom_id = session.get('chatroom_id')
    chatroom_name = session.get('current_chatroom')
    new_message = Message(username=username, room=chatroom_name, message=message_content, timestamp=timestamp, company_id=current_user.company_id, chatroom_id=chatroom_id)
    db.session.add(new_message)  # Add the message to the database session
    db.session.commit()  # Commit the session to store the message in the database

    # Use pusher to broadcast this message to all the clients
    pusher.trigger('chatroom', 'new_message', {
        'user': username,
        'message': message_content,
        'timestamp': timestamp.strftime("%A, %H:%M")
    })

    return jsonify(success=True)


@app.route('/register_organization', methods=['GET', 'POST'])
def register_organization():
    if request.method == 'POST':
        company_name = request.form['company_name']
        # Add your logic to create the organization here
        # For example, save to database
        return redirect(url_for('some_route'))  # Redirect to a confirmation page or dashboard
    return render_template('create-organization.html')

from flask import session, request, flash, render_template, redirect, url_for

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import base64
import os
import random
import string


SALT = b'my_pseudo_random'
@app.route('/create-organization', methods=['GET', 'POST'])
def create_organization():
    session.clear()
    if request.method == 'POST':
        company_name = request.form['company_name']
        if company_name:
            existing_company = Company.query.filter_by(name=company_name).first()
            if existing_company:
                flash('Company already exists.')
                return render_template('create-organization.html')

            # Generate a random password
            random_password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

            
            new_company = Company(name=company_name)
            new_company.set_password(random_password)

            try:
                db.session.add(new_company)
                db.session.commit()
                session['company_unique_id'] = new_company.unique_id
                session['company_password'] = random_password
                flash('Company created successfully.')
                return redirect(url_for('organization_start', company_name=company_name, unique_id=new_company.unique_id, password=random_password))

            except Exception as e:
                db.session.rollback()
                flash(f'An error occurred while creating the company. Error: {e}')
                return render_template('create-organization.html')
        else:
            flash('Company name cannot be empty.')
            return render_template('create-organization.html')

    return render_template('create-organization.html')


@app.route('/organization-start/<company_name>/<unique_id>/<password>')
def organization_start(company_name, unique_id, password):
    

    # Retrieve the unique ID and password from the session
    unique_id = session.get('company_unique_id', None)
    password = session.get('company_password', None)
    session['company_id'] = unique_id
    session['company_password'] = password
  
    
    if unique_id and password:
        # Render a template that shows the unique ID and password securely
        return render_template('organization-start.html', company_name=company_name, unique_id=unique_id, password=password)
    else:
        # If there is no unique ID or password in the session, redirect to home
        flash('No company information found.')
        return redirect(url_for('index'))

@app.route('/join-organization', methods=['GET'])
def redirect_organization():
    organization_id = request.args.get('company_id')
    organization_password = request.args.get('company_password')

    # Simply render the join-organization.html template on GET request
    return render_template('join-organization.html', 
                           company_id=organization_id, 
                           company_password=organization_password)


@app.route('/join-organization', methods=['POST'])
def join_organization():
    # Extract form data
    print(request.form)
    company_id = request.form.get('company_id')
    company_password = request.form.get('company_password')
    username = request.form.get('username')
    user_password = request.form.get('user_password')
    
    # Verify company
  
    company = Company.query.filter_by(unique_id=company_id).first()
    
   
    if company and company.password == company_password:

        
        # Company verified, now handle user

        # Check if username already exists within this company
        existing_user = User.query.filter_by(username=username, company_id=company.id).first()
        
        if existing_user:
            flash('Username already exists within this company.')
            return render_template('join-organization.html')

        # Generate a unique user ID using UUID
        new_user_id = str(uuid.uuid4())

        # Create a new user with the generated ID
        new_user = User(
            id=new_user_id,
            username=username, 
            password_hash=generate_password_hash(user_password), # Hash the user's password
            company_id=company.unique_id # Associate user with the company
        )
        db.session.add(new_user)
        try:
            print("hello")
            db.session.commit()
            
            flash('Successfully joined the organization.')
            # Redirect to the user's dashboard or another appropriate page
            return redirect(url_for('index'))
        except Exception as e:
            print(e)
            db.session.rollback()
         
            flash('An error occurred while creating your account. Please try again.')
            return render_template('login.html')

    else:
        flash('Invalid company ID or password.')
        print("jigaboo")
        return render_template('join-organization.html')



@app.route('/logout')
def logout():
    session.clear()
    return render_template('login.html')


@app.route('/admin/dashboard')
def admin_dashboard():


    organization_id = session.get('company_id')
    password = session.get('company_password') 


    users = User.query.filter_by(company_id=organization_id).all()

    new_company = Company.query.filter_by(unique_id=organization_id).first()
    messages = Message.query.filter_by(company_id=organization_id).all()
    chatrooms = ChatRoom.query.filter_by(company_id=organization_id).all()

    # Render the admin dashboard template
    return render_template('administrator-dashboard', 
                           organization_id=organization_id, 
                           organization_password=password, 
                           users=users, 
                           messages=messages, 
                           chatrooms=chatrooms, company=new_company, acc_user = current_user)

@app.route('/delete-user', methods=['POST'])
def delete_user():
    user_id = request.form.get('user_id')
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        # Returning a JSON response here, not redirecting.
        return jsonify({'status': 'success', 'message': 'User deleted successfully.'})
    else:
        # Returning a JSON response for failure case.
        return jsonify({'status': 'failure', 'message': 'User not found.'})


@app.route('/delete-chatroom', methods=['POST'])
def delete_chatroom():
    chat_id = request.form.get('chatroom_id')
    chat = ChatRoom.query.get(chat_id)
    if chat:
        db.session.delete(chat)
        db.session.commit()
        # Returning a JSON response here, not redirecting.
        return jsonify({'status': 'success', 'message': 'Chatroom deleted successfully.'})
    else:
        # Returning a JSON response for failure case.
        return jsonify({'status': 'failure', 'message': 'Chatroom not found.'})



@app.route('/service-worker.js')
def serve_service_worker():
    return send_from_directory('static', 'service-worker.js')

@login_manager.user_loader
def load_user(user_id):
    # Assuming your user model's ID is an integer.
    # Adjust the query if your user identifier is of a different type
    return User.query.get(user_id)


    


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)