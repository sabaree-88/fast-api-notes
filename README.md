# Notes API

A RESTful API for a note-taking application built with FastAPI and MongoDB.

## Features

- User authentication with JWT
- User registration and profile management
- Create, read, update, and delete notes
- Notes are private and associated with users

## Installation and Setup

1. Clone the repository:

```bash
git clone https://github.com/yourusername/notes-app.git
cd notes-app
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with the following variables:

```
SECRET_KEY=your-secret-key
MONGODB_URL=mongodb://localhost:27017
```

5. Run the application:

```bash
uvicorn app.main:app --reload
```

6. Access the API documentation at http://localhost:8000/docs

## API Endpoints

### Authentication

- POST `/auth/token` - Get access token

### Users

- POST `/users/` - Register a new user
- GET `/users/me` - Get current user information
- PUT `/users/me` - Update current user information

### Notes

- POST `/notes/` - Create a new note
- GET `/notes/` - Get all notes for the current user
- GET `/notes/{note_id}` - Get a specific note
- PUT `/notes/{note_id}` - Update a specific note
- DELETE `/notes/{note_id}` - Delete a specific note

## Technologies Used

- FastAPI
- MongoDB with Motor (async driver)
- JWT Authentication
- Pydantic for data validation
