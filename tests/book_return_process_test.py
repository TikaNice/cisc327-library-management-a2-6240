import pytest
from datetime import datetime, timedelta
from database import get_all_books, get_db_connection, get_patron_borrow_count, get_patron_borrowed_books
from services.library_service import (
    borrow_book_by_patron,
    add_book_to_catalog,
    return_book_by_patron
)

#Assume database alread exist

#Clean the database. 
def clean_database():
    conn = get_db_connection()
    conn.execute('DELETE FROM books')
    conn.execute('DELETE FROM borrow_records')
    conn.commit()
    conn.close()

def test_return_book_valid_input_1():
    clean_database()
    #Add a sample book. 
    add_book_to_catalog("Test Book", "Test Author", "1234567890123", 5)
    
    books = get_all_books()
    
    book_id = books[0]['id']
    patron_id = "123456"
    borrow_book_by_patron(patron_id, book_id)
    
    assert return_book_by_patron(patron_id, book_id)[0] == True
    
def test_return_book_valid_input_2():
    clean_database()
    #Add a sample book. 
    add_book_to_catalog("Test Book", "Test Author", "1234512345123", 5)
    
    books = get_all_books()
    
    book_id = books[0]['id']
    patron_id = "654321"
    borrow_book_by_patron(patron_id, book_id)
    
    assert return_book_by_patron(patron_id, book_id)[0] == True
    
def test_return_book_invalid_book_id():
    clean_database()
    #Add a sample book. 
    add_book_to_catalog("Test Book", "Test Author", "1234512345123", 5)
    
    books = get_all_books()
    
    book_id = books[0]['id']
    patron_id = "654321"
    borrow_book_by_patron(patron_id, book_id)
    
    #Use 999999 as the book id, the book does not exist
    sucess, message = return_book_by_patron(patron_id, 999999)
    assert sucess == False
    assert "Book not found." in message
    
def test_return_book_invalid_parton_id():
    clean_database()
    #Add a sample book. 
    add_book_to_catalog("Test Book", "Test Author", "1234512345123", 5)
    
    books = get_all_books()
    
    book_id = books[0]['id']
    patron_id = "654321"
    borrow_book_by_patron(patron_id, book_id)
    patron_id = "13"
    #2 digit paron id is invalid
    sucess, message = return_book_by_patron(patron_id, book_id)
    assert sucess == False
    assert "Invalid patron ID. Must be exactly 6 digits." in message

def test_return_book_not_exits_borrow_record():
    clean_database()
    #Add a sample book. 
    add_book_to_catalog("Test Book", "Test Author", "1234512345123", 1)
    
    books = get_all_books()
    
    book_id = books[0]['id']
    patron_id = "654321"
    borrow_book_by_patron(patron_id, book_id)
    patron_id = "123456"
    
    #The book is not borrowed by the patron, so it should fail
    #Which is borrow record does not exist
    sucess, message = return_book_by_patron(patron_id, book_id)
    assert sucess == False
    assert "Patron haven't borrowed this book or it has already been returned." in message

""" 
GPT-5 test case
class TestBookReturn:
    def test_valid_return(self):
        borrow_book("123456", 1)
        result = return_book("123456", 1)
        assert result["success"] is True
        assert "Book returned successfully" in result["message"]
    def test_return_not_borrowed_book(self):
        result = return_book("123456", 2)
        assert result["success"] is False
        assert "not borrowed by patron" in result["message"]
    def test_return_updates_available_copies(self):
        borrow_book("654321", 3)
        old_available = get_catalog()[2]["available_copies"]
        return_book("654321", 3)
        new_available = get_catalog()[2]["available_copies"]
        assert new_available == old_available + 1
    def test_late_fee_displayed(self):
        borrow_date = datetime.now() - timedelta(days=25)
        result = return_book("111111", 4, borrow_date=borrow_date)
        assert "late_fee" in result
        assert result["late_fee"] > 0

"""


