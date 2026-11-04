"""Reusable functions that manage books stored as dictionaries in a list."""
from .data import load_library,save_library

def all_books():
    """Return the library's list of book dictionaries."""
    return load_library()

def add_book(title,author,category,copies):
    """Validate inputs and append a book dictionary to the list."""
    title=title.strip(); author=author.strip(); category=category.strip() or 'General'
    if not title or not author: raise ValueError('Title and author are required.')
    try: copies=int(copies)
    except (TypeError,ValueError): raise ValueError('Copies must be a whole number.')
    if copies<1: raise ValueError('Add at least one copy.')
    books=load_library(); book={'id':max((b.get('id',0) for b in books),default=0)+1,'title':title,'author':author,'category':category,'total':copies,'available':copies,'borrowed':[]}
    books.append(book); save_library(books); return book

def find_book(books,book_id):
    """Find one book dictionary inside the books list."""
    book=next((b for b in books if str(b.get('id'))==str(book_id)),None)
    if book is None: raise ValueError('Book not found.')
    return book

def remove_book(book_id):
    """Remove a book only when none of its copies are borrowed."""
    books=load_library(); book=find_book(books,book_id)
    if book['available']!=book['total']: raise ValueError('Return all borrowed copies before removing this book.')
    books.remove(book); save_library(books)

def borrow_book(book_id,borrower):
    """Add a borrower's name to the book dictionary and reduce availability."""
    borrower=borrower.strip()
    if not borrower: raise ValueError('Enter the borrower's name.')
    books=load_library(); book=find_book(books,book_id)
    if book['available']<1: raise ValueError('No copies are currently available.')
    book['borrowed'].append(borrower); book['available']-=1; save_library(books); return book

def return_book(book_id,borrower):
    """Remove a borrower's name and restore one available copy."""
    books=load_library(); book=find_book(books,book_id)
    borrower=next((name for name in book['borrowed'] if name.casefold()==borrower.strip().casefold()),None)
    if borrower is None: raise ValueError('That borrower is not listed for this book.')
    book['borrowed'].remove(borrower); book['available']+=1; save_library(books); return book
