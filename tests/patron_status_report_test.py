import pytest
from database import get_all_books, get_db_connection, get_patron_borrow_count, get_patron_borrowed_books
from services.library_service import (
    add_book_to_catalog,
    borrow_book_by_patron,
    get_patron_status_report
)

#Assume database alread exist

#Clean the database. Add a sample book. 
def clean_database():
    conn = get_db_connection()
    conn.execute('DELETE FROM books')
    conn.execute('DELETE FROM borrow_records')
    conn.commit()
    conn.close()

#Test the patron status report with correct key
def test_patron_status_report_correct_key():
    clean_database()
    #Add a sample book. 
    add_book_to_catalog("Test Book", "Test Author", "1234567890123", 5)
    
    #Let patron_id = "123456" borrow the book 1
    books = get_all_books()
    patron_id = "123456"
    borrow_book_by_patron(patron_id, books[0]['id'])
    
    #Get the report of patron_id = "123456"
    report = get_patron_status_report(patron_id)
    
    #Set the correct keys
    correct_keys = ['currently_borrowed','total_late_fees','current_borrow_count','borrow_history']
    
    #Check if the report has all correct keys
    for key in correct_keys:
        assert key in report

#Test the patron status report with correct value type
def test_patron_status_report_correct_value_type():
    clean_database()
    #Add a sample book. 
    add_book_to_catalog("Test Book", "Test Author", "1234567890123", 5)
    
    #Let patron_id = "123456" borrow the book 1
    books = get_all_books()
    patron_id = "123456"
    borrow_book_by_patron(patron_id, books[0]['id'])
    
    #Get the report of patron_id = "123456"
    report = get_patron_status_report(patron_id)
    
    #Test the report has correct value type
    assert isinstance(report['currently_borrowed'], list)
    assert isinstance(report['total_late_fees'], (int, float))
    assert isinstance(report['current_borrow_count'], int)
    assert isinstance(report['borrow_history'], list)

#Test the patron status report return the correct content
def test_patron_status_report_correct_content():
    clean_database()
    #Add a sample book. 
    add_book_to_catalog("Test Book", "Test Author", "1234567890123", 5)
    
    #Let patron_id = "123456" borrow the book 1
    books = get_all_books()
    patron_id = "123456"
    borrow_book_by_patron(patron_id, books[0]['id'])
    
    #Get the report of patron_id = "123456"
    report = get_patron_status_report(patron_id)
    
    assert len(report['currently_borrowed']) == 1
    assert report['total_late_fees'] == 0
    assert report['current_borrow_count'] == 1
    assert len(report['borrow_history']) == 1
    
    
    
#Test the patron status report not exist patron_id
def test_patron_status_report_with_no_exist_patron_is():
    clean_database()
    #Add a sample book. 
    add_book_to_catalog("Test Book", "Test Author", "1234567890123", 5)
    
    #Let patron_id = "123456" borrow the book 1
    books = get_all_books()
    patron_id = "123456"
    borrow_book_by_patron(patron_id, books[0]['id'])
    
    #Get the report of patron_id = "123456"
    report = get_patron_status_report("123457")
    
    #The report should be empty since patron_id is not exist
    assert len(report['currently_borrowed']) == 0
    assert report['total_late_fees'] == 0
    assert report['current_borrow_count'] == 0
    assert len(report['borrow_history']) == 0
    
""" GPT-5 test case.
class TestPatronStatus:
    def test_patron_with_no_borrows(self):
        status = get_patron_status("888888")
        assert status["borrowed_books"] == []
        assert status["total_fees"] == 0

    def test_patron_with_borrows_and_due_dates(self):
        borrow_book("123456", 1)
        status = get_patron_status("123456")
        assert len(status["borrowed_books"]) > 0
        assert "due_date" in status["borrowed_books"][0]

    def test_total_late_fees_calculated(self):
        borrow_book("123456", 2)
        old_date = datetime.now() - timedelta(days=30)
        return_book("123456", 2, borrow_date=old_date)
        status = get_patron_status("123456")
        assert status["total_fees"] > 0

    def test_number_of_books_borrowed(self):
        borrow_book("654321", 3)
        borrow_book("654321", 4)
        status = get_patron_status("654321")
        assert status["num_books_borrowed"] == 2

    def test_borrowing_history_present(self):
        status = get_patron_status("123456")
        assert "history" in status
        assert isinstance(status["history"], list)
"""