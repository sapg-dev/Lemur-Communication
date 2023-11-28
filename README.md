![Python Badge](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff&style=flat)
![Pusher Badge](https://img.shields.io/badge/Pusher-300D4F?logo=pusher&logoColor=fff&style=flat)
![Flask Badge](https://img.shields.io/badge/Flask-000?logo=flask&logoColor=fff&style=flat)
![SQLAlchemy Badge](https://img.shields.io/badge/SQLAlchemy-D71F00?logo=sqlalchemy&logoColor=fff&style=flat)
![PythonAnywhere Badge](https://img.shields.io/badge/PythonAnywhere-1D9FD7?logo=pythonanywhere&logoColor=fff&style=flat)
![SQLite Badge](https://img.shields.io/badge/SQLite-003B57?logo=sqlite&logoColor=fff&style=flat)

# Flask Chat Application

## Introduction

This project is a real-time chat application designed for corporate use, where companies can have dedicated chat rooms for their teams to communicate instantly. The Flask Chat Application is built on top of Flask, a micro web framework written in Python, known for its simplicity and flexibility.

The application features user authentication, real-time messaging through web sockets provided by Pusher, and a database-backed persistence layer using Flask-SQLAlchemy. It allows users from the same company to join a shared chat room where they can send messages and receive updates immediately, facilitating seamless communication within the organization.

## Features

- **User Authentication:** Secure login system for users with password hashing and verification.
- **Real-time Messaging:** Leveraging Pusher's channels, users experience instantaneous communication.
- **Company-Based Chat Rooms:** Users can participate in chat rooms that are scoped to their company.
- **Database Integration:** Persistent storage of messages, user accounts, and company information.
- **Environment Configuration:** Sensitive information and configuration settings are managed via environment variables, ensuring security best practices.

## Technologies

- **Flask:** A lightweight WSGI web application framework.
- **Flask-SQLAlchemy:** An ORM for Flask applications to handle database operations.
- **Flask-Login:** Handles user session management in Flask applications.
- **Pusher:** A hosted service that provides real-time web socket channels.
- **SQLite:** A C-language library that implements a small, fast, self-contained SQL database engine.
- **Werkzeug:** A comprehensive WSGI web application library.
- **python-dotenv:** Reads key-value pairs from a `.env` file and can set them as environment variables.
- **cryptography:** A package designed to expose cryptographic primitives and recipes to Python developers.

## Setup

To get this application running locally on your machine, you need to follow these steps:

1. **Environment Setup:**
   Ensure that Python 3 and pip (Python's package installer) are installed on your machine.

2. **Clone the Repository:**
   Use Git to clone the repository to your local machine.

   ```bash
   git clone [https://github.com/sapg-dev/lemurcom.git]
   cd [local-repository-directory]

3. **Configuration**

    Configure your application by creating a .env file in the root directory of your project. This file should contain the following configurations:
    ```env
   SECRET_KEY='your_very_secret_key'
   DATABASE_URL='sqlite:///chat.db'
   PUSHER_APP_ID='your_pusher_app_id'
   PUSHER_KEY='your_pusher_key'
   PUSHER_SECRET='your_pusher_secret'
   PUSHER_CLUSTER='your_pusher_cluster'
    
4. **Install Dependencies:**
  '''bash
  pip install -r requirements.txt


5. **Running the Application**
    '''bash
    flask run




**Application Structure**

The application is structured as follows:

        - db.py: Contains the SQLAlchemy ORM models for User, Company, ChatRoom, and Message. This file defines the schema of the SQLite database and includes methods for password hashing and verification.

        -terminalChat.py: The main Flask application file that includes routes for user authentication, message handling, chat room management, and real-time functionality integration. This file also handles application initialization and configuration.

        -templates/: This directory should contain HTML files for the application's views. (Note: You must create this based on Flask's requirements and your UI design)

        -static/: A directory for static files like CSS, JavaScript, and images. (Note: This should be created to store your static content)


**Contributing**

Contributions to this project are welcome. Please fork the repository and submit a pull request with your feature or fix.
