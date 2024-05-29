# Destarinc_Assessment

# Book Review System API

## Overview
This project is a RESTful API for a hypothetical book review system built using FastAPI. The API allows users to manage books and reviews, and includes features such as data validation, error handling, database integration with SQLite, background tasks, and automated testing.

## Features
- **Endpoints**:
  - Add a new book (title, author, publication year).
  - Submit a review for a book (text review, rating).
  - Retrieve all books with an option to filter by author or publication year.
  - Retrieve all reviews for a specific book.
- **Data Validation**: Implemented using Pydantic models.
- **Error Handling**: Proper handling of invalid requests.
- **Database Integration**: Uses SQLite to persist data.
- **CRUD Operations**: Full CRUD functionality for books and reviews.
- **Background Tasks**: Simulated email confirmation after a review is posted.
- **Testing**: Automated tests for API endpoints using FastAPI's test client.

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- SQLite

### Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/your-username/book-review-system-api.git
    cd book-review-system-api
    ```

2. **Create a virtual environment**:
    ```sh
    python -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    ```

3. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Run the database migrations**:
    ```sh
    python -c "from main import Base, engine; Base.metadata.create_all(bind=engine)"
    ```

5. **Run the application**:
    ```sh
    uvicorn main:app --reload
    ```

6. **Access the API documentation**:
    Open your browser and navigate to `http://127.0.0.1:8000/docs` to explore the API endpoints and their usage.

## Usage

### Adding a New Book
- **Endpoint**: `POST /books/`
- **Request Body**:
    ```json
    {
      "title": "Book Title",
      "author": "Author Name",
      "publication_year": 2021
    }
    ```

### Submitting a Review
- **Endpoint**: `POST /books/{book_id}/reviews/`
- **Request Body**:
    ```json
    {
      "text": "Great book!",
      "rating": 5
    }
    ```

### Retrieving All Books
- **Endpoint**: `GET /books/`
- **Optional Query Parameters**: `author`, `publication_year`

### Retrieving All Reviews for a Specific Book
- **Endpoint**: `GET /books/{book_id}/reviews/`

## Testing

1. **Run the tests**:
    ```sh
    pytest
    ```

## Theoretical Questions

### Question 1: Explain how FastAPI handles asynchronous requests and its benefits over synchronous code in Python.
**Answer**: FastAPI utilizes Python's asynchronous capabilities by allowing endpoints to be defined with `async def`, enabling non-blocking operations. This improves the performance and scalability of web applications by handling concurrent requests efficiently. Asynchronous code helps to manage I/O-bound tasks such as database queries or external API calls without blocking the main execution thread, resulting in better resource utilization and faster response times.

### Question 2: Describe how dependency injection works in FastAPI and give an example of its practical use.
**Answer**: Dependency injection in FastAPI is a design pattern where dependencies are provided to a component rather than being hardcoded within it. FastAPI uses the `Depends` function to declare dependencies that are injected automatically by the framework. This enhances code modularity, testability, and reusability. For example, database sessions can be injected into endpoint functions using `Depends(get_db)`, allowing the endpoint logic to access the database without explicitly creating a session within the function.

### Question 3: Code walkthrough
**Answer**: The provided code creates a FastAPI application with endpoints for managing books and reviews. It uses Pydantic models for data validation and SQLAlchemy for database integration with SQLite. The code includes error handling, dependency injection, and a simulated background task for sending confirmation emails. Tests are written using FastAPI's test client to ensure endpoint functionality.
