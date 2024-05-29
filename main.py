"""
Assessment Overview
Part 1: API Development Task (30% of Total Score)
Build a RESTful API using FastAPI for a hypothetical book review system.

Requirements:
1. Endpoints:
   - Add a new book (title, author, publication year).
   - Submit a review for a book (text review, rating).
   - Retrieve all books with an option to filter by author or publication year.
   - Retrieve all reviews for a specific book.
2. Data Validation: Implement data validation using Pydantic models.
3. Documentation: Comments.
4. Error Handling: Implement proper error handling for invalid requests.

Part 2: Integration with Database (20% of Total Score)
Objective: Enhance the API from Part 2 to persist data using a database (e.g., SQLite, PostgreSQL).

Requirements:
1. Database Integration: Use SQLite to integrate with a database.
2. CRUD Operations: Implement CRUD (Create, Read, Update, Delete) operations for books and reviews.
3. Data Modeling: Design database schema appropriate for the book review system.

Part 3: Advanced Features and Testing (20% of Total Score)
1. Background Task: Implement a background task for sending a confirmation email (simulated) after a review is posted.
2. Testing: Write tests for the API endpoints using FastAPI's test client.

Part 4: Theoretical Questions (30% of Total Score)
- Question 1: Explain how FastAPI handles asynchronous requests and its benefits over synchronous code in Python.
- Question 2: Describe how dependency injection works in FastAPI and give an example of its practical use.
- Question 3: Code walkthrough

Evaluation Criteria
- Code Quality: Readability, use of Pythonic idioms.
- Functionality: How well the API meets the specified requirements.
- Error Handling and Robustness: Graceful handling of edge cases and invalid inputs.
- Testing: Coverage and effectiveness of tests.
- Documentation: Clarity and completeness of the API documentation.
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from pydantic import BaseModel, Field, ValidationError
from typing import List, Optional
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
from fastapi.testclient import TestClient
import os

# Get the current directory of the Python file
current_directory = os.path.dirname(os.path.abspath(__file__))



# Part 1: API Development Task
app = FastAPI()

# Database setup
# Define the SQLite database URL using the current directory
SQLALCHEMY_DATABASE_URL = f"sqlite:///{current_directory}/test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    publication_year = Column(Integer)



class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    text = Column(String)
    rating = Column(Integer)
    book = relationship("Book", back_populates="reviews")


Book.reviews = relationship("Review", back_populates="book")

Base.metadata.create_all(bind=engine)


# Pydantic models
class BookCreate(BaseModel):
    title: str
    author: str
    publication_year: int


class ReviewCreate(BaseModel):
    text: str
    rating: int


class BookGet(BaseModel):
    id: int
    title: str
    author: str
    publication_year: int




class ReviewGet(BaseModel):
    id: int
    text: str
    rating: int

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create
@app.post("/books/", response_model=BookCreate)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    db_book = Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


@app.post("/books/{book_id}/reviews/", response_model=ReviewCreate)
def create_review(book_id: int, review: ReviewCreate, db: Session = Depends(get_db),
                  background_tasks: BackgroundTasks = BackgroundTasks()):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    db_review = Review(**review.dict(), book_id=book_id)
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    # Simulate sending a confirmation email
    background_tasks.add_task(simulate_email_confirmation, db_review)
    return db_review


# Read
@app.get("/books/", response_model=List[BookGet])
def read_books(author: Optional[str] = None, publication_year: Optional[int] = None, db: Session = Depends(get_db)):
    query = db.query(Book)
    if author:
        query = query.filter(Book.author == author)
    if publication_year:
        query = query.filter(Book.publication_year == publication_year)
    return query.all()


@app.get("/books/{book_id}/reviews/", response_model=List[ReviewGet])
def read_reviews(book_id: int, db: Session = Depends(get_db)):
    reviews = db.query(Review).filter(Review.book_id == book_id).all()
    if not reviews:
        raise HTTPException(status_code=404, detail="No reviews found for this book")
    return reviews


# Update
@app.put("/books/{book_id}/", response_model=BookCreate)
def update_book(book_id: int, book: BookCreate, db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    for attr, value in book.dict().items():
        setattr(db_book, attr, value)
    db.commit()
    db.refresh(db_book)
    return db_book


@app.put("/reviews/{review_id}/", response_model=ReviewCreate)
def update_review(review_id: int, review: ReviewCreate, db: Session = Depends(get_db)):
    db_review = db.query(Review).filter(Review.id == review_id).first()
    if not db_review:
        raise HTTPException(status_code=404, detail="Review not found")
    for attr, value in review.dict().items():
        setattr(db_review, attr, value)
    db.commit()
    db.refresh(db_review)
    return db_review


# Delete
@app.delete("/books/{book_id}/")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(db_book)
    db.commit()
    return {"message": "Book deleted successfully"}


@app.delete("/reviews/{review_id}/")
def delete_review(review_id: int, db: Session = Depends(get_db)):
    db_review = db.query(Review).filter(Review.id == review_id).first()
    if not db_review:
        raise HTTPException(status_code=404, detail="Review not found")
    db.delete(db_review)
    db.commit()
    return {"message": "Review deleted successfully"}



# Error Handling
@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()}
    )


# Simulated email confirmation function
def simulate_email_confirmation(review: Review):
    print(f"Simulating email confirmation for review id {review.id}")


# Testing with FastAPI's test client
client = TestClient(app)


def test_create_book():
    response = client.post("/books/", json={"title": "Test Book", "author": "Test Author", "publication_year": 2021})
    assert response.status_code == 200
    assert response.json()["title"] == "Test Book"


def test_create_review():
    response = client.post("/books/1/reviews/", json={"text": "Great book!", "rating": 5})
    assert response.status_code == 200
    assert response.json()["text"] == "Great book!"


def test_read_books():
    response = client.get("/books/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_read_reviews():
    response = client.get("/books/1/reviews/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# Theoretical Questions

"""
Question 1: Explain how FastAPI handles asynchronous requests and its benefits over synchronous code in Python.
Answer: FastAPI utilizes Python's asynchronous capabilities by allowing endpoints to be defined with async def, enabling non-blocking operations. This improves the performance and scalability of web applications by handling concurrent requests efficiently. Asynchronous code helps to manage I/O-bound tasks such as database queries or external API calls without blocking the main execution thread, resulting in better resource utilization and faster response times.

Question 2: Describe how dependency injection works in FastAPI and give an example of its practical use.
Answer: Dependency injection in FastAPI is a design pattern where dependencies are provided to a component rather than being hardcoded within it. FastAPI uses the Depends function to declare dependencies that are injected automatically by the framework. This enhances code modularity, testability, and reusability. For example, database sessions can be injected into endpoint functions using Depends(get_db), allowing the endpoint logic to access the database without explicitly creating a session within the function.

Question 3: Code walkthrough
Answer: The provided code creates a FastAPI application with endpoints for managing books and reviews. It uses Pydantic models for data validation and SQLAlchemy for database integration with SQLite. The code includes error handling, dependency injection, and a simulated background task for sending confirmation emails. Tests are written using FastAPI's test client to ensure endpoint functionality.
"""
