import pytest
from database import get_all_books, init_database, add_sample_data, get_db_connection
from services.library_service import (
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

def test_get_all_books_returns_book_list():
    clean_database()
    add_book_to_catalog("Test Book", "Test Author", "1234567892235", 5)
    """Test get_all_books return a list of book and include at least one book"""
    books = get_all_books()
    
    # 验证返回了书籍列表
    assert isinstance(books, list)
    assert len(books) > 0

def test_get_all_books_returns_correct_columns():
    clean_database()
    add_book_to_catalog("Test Book", "Test Author", "1234567892235", 5)
    """Test each book have the correct columns"""
    books = get_all_books()
    
    
    """Check each book have the correct column or not, if didn't include the print which column this book missing. """
    
    required_column = ['id', 'title', 'author', 'isbn', 'total_copies', 'available_copies']
    for book in books:
        for column in required_column:
            assert column in book, f"Missing column: {column}"
    

def test_get_all_books_returns_correct_columns_types():
    clean_database()
    add_book_to_catalog("Test Book", "Test Author", "1234567892235", 5)
    """Test each book have the correct columns with correct types"""
    books = get_all_books()
    
    # Check each book have the correct column with correct types
    
    for book in books:
        assert isinstance(book['id'], int)
        assert isinstance(book['title'], str)
        assert isinstance(book['author'], str)
        assert isinstance(book['isbn'], str)
        assert isinstance(book['total_copies'], int)
        assert isinstance(book['available_copies'], int)

def test_get_all_books_after_adding_one():
    """Clean the database, add 1 book and check if get_all_books returns only that book and content is correct"""
    # Clean dataset
    clean_database()
    
    #Set variable and add book
    title = "Test Book"
    author = "Test Author"
    isbn = "1234567892235"
    copies = 5
    
    success, message = add_book_to_catalog(title, author, isbn, copies)
    assert success == True, f"Failed to add book: {message}"
    assert "successfully added" in message.lower()

    #Get book can check the content and len of books
    books = get_all_books()
    assert len(books) == 1
    book = books[0]
    assert book['title'] == title
    assert book['author'] == author
    assert book['isbn'] == isbn
    assert book['total_copies'] == copies
    assert book['available_copies'] == copies
    
"""
GPT-5 given test cases
class TestBookCatalogDisplay:
    def test_catalog_displays_all_books(self):
        catalog = get_catalog()
        assert isinstance(catalog, list)
        assert all("title" in b and "author" in b for b in catalog)
    def test_display_includes_available_and_total(self):
        catalog = get_catalog()
        for book in catalog:
            assert "available_copies" in book and "total_copies" in book
    def test_borrow_button_for_available_books(self):
        catalog = get_catalog()
        available_books = [b for b in catalog if b["available_copies"] > 0]
        for b in available_books:
            assert b["actions"].get("borrow") is True
    def test_no_borrow_button_when_unavailable(self):
        catalog = get_catalog()
        unavailable_books = [b for b in catalog if b["available_copies"] == 0]
        for b in unavailable_books:
            assert b["actions"].get("borrow") is False

"""