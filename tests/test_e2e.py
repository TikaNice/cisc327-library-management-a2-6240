import pytest
from playwright.sync_api import Page, expect
import time
from database import get_db_connection
#Use Headless mode for test


#Test add a new book to the database

#Set a sample new book data for testing
#There will be error happen if run the test more than 1 time, because the database is not reset
#So I set isbn and title change by time
time_isbn = str(int(time.time()))
sample_new_book = {
    "title": f"Testing Handbook {time_isbn} Title",
    "author": "Playwright Bot",
    "isbn": f"123{time_isbn}",
    "copies": "10"
}

#Set book id and patron id for testing
sample_patron_id = "123457"


#Use session-scoped fixture stored in the new book ID for later testing.
@pytest.fixture(scope="session")
def new_book_id():
    """Fixture to store the ID of the book added in the first test."""
    # None now and will change in the add book test
    return {"id": None}


#For (i and ii), add new book and verify the new book appears in the catalog
def test_add_new_book(page: Page,new_book_id):
    page.goto("http://127.0.0.1:5000/")

    #Make sure current page is add book page
    page.click("text=➕ Add New Book")
    
    expect(page.locator("h2")).to_have_text("➕ Add New Book")
    
    page.fill("#title", sample_new_book["title"])
    page.fill("#author", sample_new_book["author"])
    page.fill("#isbn", sample_new_book["isbn"])
    page.fill("#total_copies", sample_new_book["copies"])
    

    #Click the button to add the book to the catalog
    page.click('button[type="submit"]:has-text("Add Book to Catalog")')

    #Assert that the success message is displayed
    success_message = f'Book "{sample_new_book["title"]}" has been successfully added to the catalog.'

    #Make sure sucess flask message is displayed
    expect(page.locator(".flash-success")).to_be_visible()
    expect(page.locator(".flash-success")).to_contain_text(success_message)
    
    #Go to the catalog page and check new book is added and show
    page.click("text=📖 Catalog")
    book_row_locator = page.locator("tr", has_text=sample_new_book["title"]) 
    expect(book_row_locator).to_be_visible()
    
    #Need to get book id for next borrow book function
    book_row = page.locator(f'tr:has-text("{sample_new_book["title"]}")')
    book_id_element = book_row.locator('td').first
    new_book_id["id"] = book_id_element.inner_text().strip()
    
    
    

#Test borrow book by patron id and book id
#For (iii,iv), 
# (iii)Navigate to borrow book page
# (iv)borrow a book by patron id and book id
def test_borrow_a_book(page: Page,new_book_id):
    
    #Asume last test save the book id for this test case to borrow.
    book_id_to_borrow = new_book_id["id"]

    #Navigate to borrow book page
    page.goto("http://127.0.0.1:5000/catalog")
    
    #Navigate to borrow book row and fill book_id 1(Since we just add a book so it should at least 1 book)
    book_row_selector = f'//tr[td[text()="{book_id_to_borrow}"]]'
    book_row_locator = page.locator(book_row_selector)
    
    #Fill the patron id box
    book_row_locator.locator('input[name="patron_id"]').fill(sample_patron_id)
    
    #fill the borrow book button
    book_row_locator.locator('button[type="submit"]:has-text("Borrow")').click()
    
    #Assert that the success message is displayed
    expect(page.locator(".flash-success")).to_be_visible()
    expect(page.locator(".flash-success")).to_contain_text(f'Successfully borrowed')
    expect(page.locator(".flash-success")).to_contain_text("Due date:")
