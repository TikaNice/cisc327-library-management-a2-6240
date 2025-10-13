import pytest
from database import get_all_books, get_db_connection, get_patron_borrow_count, get_patron_borrowed_books
from library_service import (
    add_book_to_catalog
)

#Clean the database. 
def clean_database():
    conn = get_db_connection()
    conn.execute('DELETE FROM books')
    conn.execute('DELETE FROM borrow_records')
    conn.commit()
    conn.close()
    
#Assume database alread exist

def test_add_book_valid_input():
    clean_database()
    """Test adding a book with valid input."""
    success, message = add_book_to_catalog("Test Book", "Test Author", "1234567892235", 5)
    
    assert success == True
    assert "successfully added" in message.lower()

def test_add_book_invalid_isbn_too_short():
    clean_database()
    """Test adding a book with ISBN too short."""
    success, message = add_book_to_catalog("Test Book", "Test Author", "1", 5)
    
    assert success == False
    assert "ISBN must be exactly 13 digits." in message

def test_add_book_invalid_total_copies_is_negative():
    clean_database()
    """Test adding a book with negative copies."""
    success, message = add_book_to_catalog("Test Book", "Test Author", "0123456789012", -2)
    
    assert success == False
    assert "total copies must be a positive integer" in message.lower()

def test_add_same_book():
    clean_database()
    """Test adding a book with book have same ISBN already exist."""
    add_book_to_catalog("Test Book", "Test Author", "1234567891234", 5)
    success, message = add_book_to_catalog("Test Book", "Test Author", "1234567891234", 5)
    
    assert success == False
    assert "a book with this isbn already exists" in message.lower()

def test_no_title():
    clean_database()
    """Test adding a book without title."""
    success, message = add_book_to_catalog("", "Test Author", "1234567891236", 5)
    
    assert success == False
    assert "title is required" in message.lower()
    
"""
GPT-5 given test cases
class TestAddBookToCatalog:
    def test_add_valid_book(self):
        result = add_book_to_catalog("Clean Code", "Robert Martin", "9780132350884", 5)
        assert result["success"] is True
        assert "Book added successfully" in result["message"]
    def test_missing_required_field(self):
        result = add_book_to_catalog("", "Robert Martin", "9780132350884", 5)
        assert result["success"] is False
        assert "Title is required" in result["message"]
    def test_title_too_long(self):
        long_title = "A" * 201
        result = add_book_to_catalog(long_title, "Author", "9780132350884", 5)
        assert result["success"] is False
        assert "max 200 characters" in result["message"]
    def test_invalid_isbn_length(self):
        result = add_book_to_catalog("Book", "Author", "12345", 5)
        assert result["success"] is False
        assert "ISBN must be 13 digits" in result["message"]
    def test_negative_total_copies(self):
        result = add_book_to_catalog("Book", "Author", "9780132350884", -2)
        assert result["success"] is False
        assert "positive integer" in result["message"]
"""