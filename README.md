<<<<<<< HEAD

# fsbe
# FastAPI Planning System Backend

Welcome to the FastAPI Planning System Backend! This application serves as the core component for a robust planning system built using FastAPI and SQLAlchemy. It provides a comprehensive set of functionalities for managing users, companies, planning activities, and notifications.

## Features

### User Management
Facilitates user registration, login, and management functionalities. Users can be associated with companies and assigned administrative privileges.

### Company Management
Enables CRUD (Create, Read, Update, Delete) operations for companies. Admin users have the capability to create, update, and delete company records as necessary.

### Planning Activities
Supports the creation, retrieval, updating, and deletion of planning activities. Automatic generation of notifications for users associated with each activity streamlines communication and coordination.

### Notifications
Provides endpoints for managing notifications, including marking them as read or unread, ensuring timely and effective communication within the planning system.

## Installation

### 1. Clone the Repository
Begin by cloning this repository to your local machine:
\`\`\`bash
git clone https://github.com/antoinecaby/fsbe.git
\`\`\`

### 2. Navigate to the Project Directory
Move into the project directory using the following command:
\`\`\`bash
cd fsbe
\`\`\`

### 3. Install Dependencies
Install the required dependencies using pip:
\`\`\`bash
pip install -r requirements.txt
\`\`\`

## Configuration

### Database Setup
Execute the create_database function found in db/database.py to set up a SQLite database. This function will create the necessary tables for the application.

### JWT Token Configuration
Generate a secret key for JWT token encryption. Replace the placeholder value in SECRET_KEY located in internal/auth.py with your generated key.

## Usage

### Start the FastAPI Server

#### Docker mode
**Requirements:** Docker and docker-compose installed  
To launch, your terminal must be in the root folder of this repository. Then issue:  
\`\`\`bash
docker-compose up --build
\`\`\`

#### Uvicorn mode
**Requirements:** Python 3.10 or greater installed  
First, install dependencies:
\`\`\`bash
pip install -r requirements.txt
\`\`\`

Then, launch the FastAPI server:
\`\`\`bash
uvicorn main:app --reload
\`\`\`

### Access the Interactive Documentation
Open your web browser and navigate to [http://localhost:8000/docs](http://localhost:8000/docs) to access the FastAPI interactive documentation. Here, you can explore and interact with the available endpoints seamlessly.

# Configuration

## Database Setup

To set up the database, execute the `create_database` function found in `db/database.py`. This function will create the necessary tables for the application.

## SQLite Database Schema

The database schema includes the following tables:

1. **User Table (`users`):**
   - `id`: Primary key, unique identifier for each user.
   - `email`: Email address of the user, used for login and identification.
   - `password`: Hashed password of the user for authentication.
   - ...

2. **Company Table (`companies`):**
   - `id`: Primary key, unique identifier for each company.
   - `name`: Name of the company.
   - `description`: Description of the company.
   - ...

3. **Planning Activity Table (`activities`):**
   - `id`: Primary key, unique identifier for each planning activity.
   - `title`: Title of the planning activity.
   - `description`: Description of the planning activity.
   - ...

4. **Notification Table (`notifications`):**
   - `id`: Primary key, unique identifier for each notification.
   - `user_id`: Foreign key referencing the user the notification belongs to.
   - `message`: Content of the notification message.
   - ...



## Authentication

### JWT-based Authentication
Authentication is based on JSON Web Tokens (JWT). Users can obtain a token by logging in with their email and password.

### Token Management
- The token must be included in the Authorization header of subsequent requests to authenticated endpoints.
- Tokens have a default expiration time of 24 hours, enhancing security by limiting their lifespan. Users can log out to invalidate their token.

## Authorization

### Admin Privileges
Admin users enjoy elevated privileges, allowing them to perform additional operations such as managing companies and accessing other users' information.

### Access Control
Access control mechanisms are implemented to ensure that users can only view or modify data associated with their respective company, maintaining data integrity and privacy.

## API Endpoints

### User Management
- **POST /users/register:** Register a new user.
- **POST /users/login:** Log in an existing user and obtain a JWT token.
- **GET /users/me:** Retrieve details of the currently authenticated user.
- **GET /users/{user_id}:** Retrieve details of a specific user by ID.
- **PUT /users/me:** Update details of the currently authenticated user.
- **DELETE /users/me:** Delete the currently authenticated user account.

### Company Management
- **POST /companies/:** Create a new company.
- **GET /companies/:** Retrieve a list of all companies.
- **GET /companies/{company_id}:** Retrieve details of a specific company by ID.
- **PUT /companies/{company_id}:** Update details of a specific company by ID.
- **DELETE /companies/{company_id}:** Delete a specific company by ID.

### Planning Activities
- **POST /activities/:** Create a new planning activity.
- **GET /activities/:** Retrieve a list of all planning activities.
- **GET /activities/{activity_id}:** Retrieve details of a specific planning activity by ID.
- **PUT /activities/{activity_id}:** Update details of a specific planning activity by ID.
- **DELETE /activities/{activity_id}:** Delete a specific planning activity by ID.

### Notifications
- **GET /notifications/:** Retrieve a list of notifications for the currently authenticated user.
- **POST /notifications/mark_as_read:** Mark notifications as read for the currently authenticated user.
- **POST /notifications/mark_as_unread:** Mark notifications as unread for the currently authenticated user.

## Security Considerations

### Password Hashing
All passwords are securely hashed using the bcrypt hashing algorithm, safeguarding user credentials against unauthorized access.

### JWT Token Security
JWT tokens are signed with a secret key and encrypted using the HS256 algorithm, minimizing the risk of tampering and ensuring data integrity during transmission.

### Access Control
Robust access control mechanisms are in place to prevent unauthorized access to resources, enhancing the overall security posture of the application.

## Error Handling

### HTTPException Handling
Gracefully handles errors and provides meaningful error messages to the client.

### Rollback on Error
Rolls back transactions in case of exceptions during database operations to maintain data consistency and integrity.

## Authentication Flow

1. **Login Endpoint:** Users authenticate with their email and password to obtain an access token.
2. **Token Inclusion:** The token must be included in the Authorization header of subsequent requests to authenticated endpoints.
3. **Token Expiry:** Tokens have a default expiration time of 24 hours. Users can log out to invalidate their token.
4. **Logout Endpoint:** Includes a logout endpoint to invalidate the token by removing it from the logged_in_users dictionary.

This README file provides a comprehensive overview of the FastAPI Planning System Backend, covering installation instructions, configuration steps, usage guidelines, security considerations, and API documentation. Follow the instructions diligently to set up and utilize the application effectively. For further assistance or inquiries, please do not hesitate to reach out!

=======
# fsbe

Projet Full-Stack Back-End

# Documentation

Une documentation est automatiquement disponible à localhost:port/docs ou /redocs. Par défaut le domaine est localhost sur le port 80.

# Prérequis

Avant de pouvoir lancer l'application il faut que vous ayez installé :

- Docker Desktop : https://www.docker.com/products/docker-desktop/
- DB Browser for SQLite : https://sqlitebrowser.org/dl/
- Python : https://www.python.org/downloads/

# Lancer le projet

1. Lancer l'application Docker

2. Supprimer le fichier fsbe.db dans app/db si déjà existant (c'est le fichier de la base de donnée, il est généré automatiquement au lancement du projet)

3. Ouvrir un terminal de commande et effectuer les commandes suivantes

   - poetry install
   - docker compose up --build

4. Lancez l'application DB Browser for SQLite et ouvrez le fichier app/db/fsbe qui vient d'être généré par "docker-compose up --build"
>>>>>>> 6014d6a4b537835f5c56e15838bbe534ebc4ac05
