import pytest
from datetime import datetime, timedelta
from database import get_all_books, get_db_connection, get_patron_borrow_count, get_patron_borrowed_books
from services.library_service import (
    borrow_book_by_patron,
    add_book_to_catalog
)

#Assume database alread exist

#Clean the database. Add a sample book. 
def clean_database():
    conn = get_db_connection()
    conn.execute('DELETE FROM books')
    conn.execute('DELETE FROM borrow_records')
    conn.commit()
    conn.close()

def test_borrow_book_valid_input():
    clean_database()
    #Add a sample book. 
    add_book_to_catalog("Test Book", "Test Author", "1234567890123", 5)
    
    books = get_all_books()
    
    book_id = books[0]['id']
    patron_id = "123456"
    
    success, message = borrow_book_by_patron(patron_id, book_id)
    assert success == True
    assert "successfully borrowed" in message.lower()
    assert "due date" in message.lower()
    
    
    #In the sample book we add, the available_copies was 5.
    #So after borrowing one, it should be 4.
    updated_books = get_all_books()
    assert updated_books[0]['available_copies'] == 4
    
    #Check the borrow records.
    borrowed_record = get_patron_borrowed_books(patron_id)
    #Since we clean the borrow records before each test, so borrowed_record should be length 1
    assert len(borrowed_record) == 1
    assert borrowed_record[0]['book_id'] == book_id
    assert borrowed_record[0]['title'] == books[0]['title']
    assert borrowed_record[0]['author'] == books[0]['author']
    

def test_borrow_book_invalid_book_id():
    clean_database()
    #Add a sample book. 
    add_book_to_catalog("Test Book", "Test Author", "1234567890123", 5)
    
    patron_id = "123456"
    
    success, message = borrow_book_by_patron(patron_id, 999999)
    assert success == False
    assert "book not found." in message.lower()
    
def test_borrow_book_invalid_patron_id():
    clean_database()
    #Add a sample book. 
    add_book_to_catalog("Test Book", "Test Author", "1234567890123", 5)
    
    books = get_all_books()
    
    book_id = books[0]['id']
    patron_id = "12"
    
    success, message = borrow_book_by_patron(patron_id, book_id)
    assert success == False
    assert "invalid patron id" in message.lower()

def test_borrow_book_no_available_copies():
    clean_database()
    #Add a sample book. 
    add_book_to_catalog("Test Book", "Test Author", "1234567890123", 1)
    
    books = get_all_books()
    
    book_id = books[0]['id']
    patron_id = "123456"
    
    #Borrow the book once
    borrow_book_by_patron(patron_id, book_id)
    #Borrow the book again, should fail because no available copies
    success, message = borrow_book_by_patron(patron_id, book_id)
    assert success == False
    assert "this book is currently not available." in message.lower()
    

"""
Adding more test cases for the add_book_to_catalog function to inprove the cover rate.
"""
def test_borrow_book_too_much_borrow():
    clean_database()
    #Add a sample book. 
    add_book_to_catalog("Test Book", "Test Author", "1234567890123", 15)
    
    books = get_all_books()
    
    book_id = books[0]['id']
    patron_id = "123456"
    
    #Borrow the book 5 times
    borrow_book_by_patron(patron_id, book_id)
    borrow_book_by_patron(patron_id, book_id)
    borrow_book_by_patron(patron_id, book_id)
    borrow_book_by_patron(patron_id, book_id)
    borrow_book_by_patron(patron_id, book_id)
    
    #Borrow the book once more, should fail because patron has reached the borrow limit
    success, message = borrow_book_by_patron(patron_id, book_id)
    assert success == False
    assert "You have reached the maximum borrowing limit of 5 books" in message
    
    