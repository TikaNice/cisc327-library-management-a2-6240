import pytest
from database import get_all_books, get_db_connection, get_patron_borrow_count, get_patron_borrowed_books
from library_service import (
    add_book_to_catalog,
    search_books_in_catalog
)

#Assume database alread exist

#Clean the database. 
def clean_database():
    conn = get_db_connection()
    conn.execute('DELETE FROM books')
    conn.execute('DELETE FROM borrow_records')
    conn.commit()
    conn.close()

def test_search_books_in_catalog_valid_input_and_output_1():
    clean_database()
    #Add one sample book to the database
    add_book_to_catalog("Test Book", "Test Author", "1234567892235", 5)
    
    #The return should be only len 1.
    assert len(search_books_in_catalog("Test Book", "title")) == 1
    assert len(search_books_in_catalog("Test Author", "author")) == 1
    assert len(search_books_in_catalog("1234567892235", "isbn")) == 1

def test_search_books_in_catalog_author_match_2_books():
    clean_database()
    #Add one sample book to the database
    add_book_to_catalog("Test Book", "Test Author", "1234567892235", 5)
    add_book_to_catalog("Test Book 2", "Test Author", "1234567891235", 5)
    
    #The return should be only len 2.
    assert len(search_books_in_catalog("TEST AUTHOR", "author")) == 2
    #Either lower case or upper case
    assert len(search_books_in_catalog("test author", "author")) == 2
    
def test_search_books_in_catalog_title_match_2_books():
    clean_database()
    #Add one sample book to the database
    add_book_to_catalog("Test Book", "Test Author 1", "1234567892235", 5)
    add_book_to_catalog("test Book", "Test Author 2", "1234567891235", 5)
    
    #The return should be only len 2. Either lower case or upper case 
    assert len(search_books_in_catalog("Test Book", "title")) == 2
    
def test_search_books_in_catalog_with_invalid_isbn():
    clean_database()
    #Add one sample book to the database
    add_book_to_catalog("Test Book", "Test Author", "1234567892235", 5)
    
    #The return should be empty which is len 0.
    assert len(search_books_in_catalog("234567892235", "isbn")) == 0
    
def test_search_books_in_catalog_with_invalid_search_type():
    clean_database()
    #Add one sample book to the database
    add_book_to_catalog("Test Book", "Test Author", "1234567892235", 5)
    
    #The return should be empty which is len 0.
    assert len(search_books_in_catalog("test book", "invaild")) == 0

def test_search_books_in_catalog_with_not_exist_isbn():
    clean_database()
    #Add one sample book to the database
    add_book_to_catalog("Test Book", "Test Author", "1234567892235", 5)
    
    #The return should be empty which is len 0 for not exist ISBN
    assert len(search_books_in_catalog("1234567891234", "isbn")) == 0
    
""" GPT-5
class TestBookSearch:
    def test_search_by_title_partial_match(self):
        results = search_books_in_catalog("clean", "title")
        assert any("Clean Code" in b["title"] for b in results)
    def test_search_by_author_partial_case_insensitive(self):
        results = search_books_in_catalog("martin", "author")
        assert any("Martin" in b["author"] for b in results)
    def test_search_by_isbn_exact_match(self):
        results = search_books_in_catalog("9780132350884", "isbn")
        assert len(results) == 1
    def test_search_invalid_type(self):
        results = search_books_in_catalog("clean", "publisher")
        assert results == []
    def test_search_empty_term(self):
        results = search_books_in_catalog("", "title")
        assert results == []
"""