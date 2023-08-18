## About Project
Simple API for chat applications with user registration, using websockets and saving chat history to PostgreSQL database.

### Project Stack: 
 - FastAPI
 - PostgreSQL
 - FastAPI-Users
 - Websockets
 - Alembic
 - Pydantic

### Start the application
1. Create a virtual environment and install dependencies
2. Run `pip install -r requirements.txt` in the terminal

### Configuring Alembic for the asynchronous driver
1. From the root directory, start the 
`alembic init -t async migrations`

### Application launch
1. Go to the `src` folder
2. Run `uvicorn main:app --reload` in the terminal
