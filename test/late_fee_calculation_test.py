import pytest
from datetime import datetime, timedelta
from database import get_db_connection, init_database, add_sample_data, get_all_books
from library_service import calculate_late_fee_for_book, borrow_book_by_patron, add_book_to_catalog


#Assume database alread exist

#Clean the database. Add a sample book. 
def clean_database():
    conn = get_db_connection()
    conn.execute('DELETE FROM books')
    conn.execute('DELETE FROM borrow_records')
    conn.commit()
    conn.close()
    add_book_to_catalog("Test Book", "Test Author", "1234567890123", 5)
    
#No late fee
def test_calculate_late_fee_no_overdue():
    #Clean database
    clean_database()
    
    books = get_all_books()
    book_id = books[0]['id']
    patron_id = "123456"
    
    #Set borrow date to 12 days ago and return day is today
    current_date = datetime.now()
    borrow_date = current_date - timedelta(days=12)
    due_date = borrow_date + timedelta(days=14)
    
    #Connect to database by ourself since no method allow us edit the return day
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO borrow_records (patron_id, book_id, borrow_date, due_date)
        VALUES (?, ?, ?, ?)
    ''', (patron_id, book_id, borrow_date.isoformat(), due_date.isoformat()))
    conn.commit()
    conn.close()
    
    return_json = calculate_late_fee_for_book(patron_id, book_id)
    
    assert return_json['fee_amount'] == 0
    assert return_json['days_overdue'] == 0
    
#3 day overdue, less then 7 day overdue
def test_calculate_late_fee_2_day_overdue():
    #Clean database
    clean_database()
    
    books = get_all_books()
    book_id = books[0]['id']
    patron_id = "123456"
    
    #Set borrow date to 16 days ago(2 day late)
    current_date = datetime.now()
    borrow_date = current_date - timedelta(days=16)
    due_date = borrow_date + timedelta(days=14)
    
    #Connect to database by ourself since no method allow us edit the return day
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO borrow_records (patron_id, book_id, borrow_date, due_date)
        VALUES (?, ?, ?, ?)
    ''', (patron_id, book_id, borrow_date.isoformat(), due_date.isoformat()))
    conn.commit()
    conn.close()
    
    return_json = calculate_late_fee_for_book(patron_id, book_id)
    
    assert return_json['fee_amount'] == 1
    assert return_json['days_overdue'] == 2

#10 day overdue, between 7 day overdue and 14 overdue
def test_calculate_late_fee_10_day_overdue():
    #Clean database
    clean_database()
    
    books = get_all_books()
    book_id = books[0]['id']
    patron_id = "123456"
    
    #Set borrow date to 24 days ago(10 day late)
    current_date = datetime.now()
    borrow_date = current_date - timedelta(days=24)
    due_date = borrow_date + timedelta(days=14)
    
    #Connect to database by ourself since no method allow us edit the return day
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO borrow_records (patron_id, book_id, borrow_date, due_date)
        VALUES (?, ?, ?, ?)
    ''', (patron_id, book_id, borrow_date.isoformat(), due_date.isoformat()))
    conn.commit()
    conn.close()
    
    return_json = calculate_late_fee_for_book(patron_id, book_id)
    
    assert return_json['fee_amount'] == 6.5
    assert return_json['days_overdue'] == 10

#30 day overdue, reaching the max late fee 15
def test_calculate_late_fee_30_day_overdue():
    #Clean database
    clean_database()
    
    books = get_all_books()
    book_id = books[0]['id']
    patron_id = "123456"
    
    #Set borrow date to 44 days ago(30 day late)
    current_date = datetime.now()
    borrow_date = current_date - timedelta(days=44)
    due_date = borrow_date + timedelta(days=14)
    
    #Connect to database by ourself since no method allow us edit the return day
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO borrow_records (patron_id, book_id, borrow_date, due_date)
        VALUES (?, ?, ?, ?)
    ''', (patron_id, book_id, borrow_date.isoformat(), due_date.isoformat()))
    conn.commit()
    conn.close()
    
    return_json = calculate_late_fee_for_book(patron_id, book_id)
    
    assert return_json['fee_amount'] == 15
    assert return_json['days_overdue'] == 30

"""GPT-5 Test case
class TestLateFeeCalculation:
    def test_no_late_fee_within_14_days(self):
        borrow_date = datetime.now() - timedelta(days=10)
        fee = calculate_late_fee(borrow_date)
        assert fee == 0.0
    def test_fee_first_7_days_overdue(self):
        borrow_date = datetime.now() - timedelta(days=18)
        fee = calculate_late_fee(borrow_date)
        assert round(fee, 2) == 2.0  # 4 days * 0.5
    def test_fee_after_7_days_overdue(self):
        borrow_date = datetime.now() - timedelta(days=25)
        fee = calculate_late_fee(borrow_date)
        # 7 days * 0.5 + 4 days * 1.0 = 7.5
        assert round(fee, 2) == 7.5
    def test_fee_capped_at_15(self):
        borrow_date = datetime.now() - timedelta(days=60)
        fee = calculate_late_fee(borrow_date)
        assert fee == 15.0

"""