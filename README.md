### Flask API for library-management-system.
 
1. **Overview**:
 A simple Flask API for a Library Management System, supporting CRUD operations for books and members and allows searching books by title or author and filtering members by type (student or staff).

2.**How to Run the Project**:
-Prerequisites:
Python 3.x installed on your machine.
Flask installed (pip install flask).
-steps to run:
i) Clone the repository.
ii) Ensure the following files are in the same directory:
    -run.py
    -books.py
    -members.py
iii) Install necessary dependencies:
    -pip install flask
iv) Start the server:
    -python run.py
    -The server will run on http://127.0.0.1:5000

3. **Design Choices**:
i)Modularization:
    The API is divided into two modules:
    -books.py: Handles all CRUD operations for books.
    -members.py: Handles all CRUD operations for members.
    -Each module is registered as a Flask blueprint in run.py.
ii)In-Memory Data Storage:
    -Data is stored in Python dictionaries (books and members) for simplicity.
    -This design is for API testing and does not persist data across sessions.
iii)Validation:
    -Input data is validated for required fields and correct types.
    -Duplicate entries are prevented in books by checking the title and author
iv)Filtering
    -Books can be filtered by title or author using query parameters.
    -Members can be filtered by type (either student or staff).

4. **Assumptions and Limitations**:
i)Assumptions:
    -Each book and member has a unique id.
    -Members are categorized as either student or staff.
    -No authentication or authorization is required.  
ii)Limitations
    -Data is not permanent (no database integration),restarting   the server clears all data.
    -Search and filter operations are case-insensitive but basic.
    -Designed for testing and development purposes.