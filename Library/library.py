"""
Library Management System
Author:Vishnu Shankar
Assignment: Library Inventory System - Task 3 & 4
Description: Main library management system with file persistence
"""

import json
import os
from book import Book
from member import Member


class Library:
    """
    Central library management system.
    
    Manages:
        - List of books
        - List of members
        - Borrow/return operations
        - File persistence (JSON format)
    """
    
    # Class-level variable for analytics
    total_transactions = 0
    
    def __init__(self, data_dir="library_data"):
        """
        Initialize the Library system.
        
        Args:
            data_dir (str): Directory to store library data files
        """
        self.books = {}  # Dictionary: ISBN -> Book object
        self.members = {}  # Dictionary: member_id -> Member object
        self.data_dir = data_dir
        self.books_file = os.path.join(data_dir, "books.json")
        self.members_file = os.path.join(data_dir, "members.json")
        
        # Create data directory if it doesn't exist
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        
        # Load existing data
        self.load_data()
    
    def add_book(self, title, author, isbn):
        """
        Add a new book to the library.
        
        Args:
            title (str): Book title
            author (str): Book author
            isbn (str): ISBN number
            
        Returns:
            bool: True if added, False if ISBN already exists
        """
        if isbn in self.books:
            return False
        
        book = Book(title, author, isbn)
        self.books[isbn] = book
        self.save_books()
        return True
    
    def register_member(self, name, member_id):
        """
        Register a new library member.
        
        Args:
            name (str): Member's full name
            member_id (str): Unique member identifier
            
        Returns:
            bool: True if registered, False if ID already exists
        """
        if member_id in self.members:
            return False
        
        member = Member(name, member_id)
        self.members[member_id] = member
        self.save_members()
        return True
    
    def lend_book(self, member_id, isbn):
        """
        Lend a book to a member.
        
        Args:
            member_id (str): Member's ID
            isbn (str): Book's ISBN
            
        Returns:
            bool: True if successful, False otherwise
        """
        if member_id not in self.members:
            print(f"Error: Member ID '{member_id}' not found.")
            return False
        
        if isbn not in self.books:
            print(f"Error: ISBN '{isbn}' not found.")
            return False
        
        member = self.members[member_id]
        book = self.books[isbn]
        
        if member.borrow_book(book):
            Library.total_transactions += 1
            self.save_books()
            self.save_members()
            return True
        else:
            print(f"Error: Book '{book.title}' is not available.")
            return False
    
    def take_return(self, member_id, isbn):
        """
        Accept return of a book from a member.
        
        Args:
            member_id (str): Member's ID
            isbn (str): Book's ISBN
            
        Returns:
            bool: True if successful, False otherwise
        """
        if member_id not in self.members:
            print(f"Error: Member ID '{member_id}' not found.")
            return False
        
        if isbn not in self.books:
            print(f"Error: ISBN '{isbn}' not found.")
            return False
        
        member = self.members[member_id]
        book = self.books[isbn]
        
        if member.return_book(book):
            Library.total_transactions += 1
            self.save_books()
            self.save_members()
            return True
        else:
            print(f"Error: Member did not borrow '{book.title}'.")
            return False
    
    def get_book_by_isbn(self, isbn):
        """Get a book by ISBN."""
        return self.books.get(isbn)
    
    def get_member_by_id(self, member_id):
        """Get a member by ID."""
        return self.members.get(member_id)
    
    def list_all_books(self):
        """Return a list of all books."""
        return list(self.books.values())
    
    def list_all_members(self):
        """Return a list of all members."""
        return list(self.members.values())
    
    # ============ FILE PERSISTENCE ============
    
    def save_books(self):
        """Save all books to JSON file."""
        try:
            books_data = [book.to_dict() for book in self.books.values()]
            with open(self.books_file, "w") as f:
                json.dump(books_data, f, indent=4)
        except IOError as e:
            print(f"Error saving books to file: {e}")
    
    def load_books(self):
        """Load books from JSON file."""
        try:
            if os.path.exists(self.books_file):
                with open(self.books_file, "r") as f:
                    books_data = json.load(f)
                    for book_dict in books_data:
                        book = Book.from_dict(book_dict)
                        self.books[book.isbn] = book
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error loading books from file: {e}")
            print("Starting with empty library...")
    
    def save_members(self):
        """Save all members to JSON file."""
        try:
            members_data = [member.to_dict() for member in self.members.values()]
            with open(self.members_file, "w") as f:
                json.dump(members_data, f, indent=4)
        except IOError as e:
            print(f"Error saving members to file: {e}")
    
    def load_members(self):
        """Load members from JSON file."""
        try:
            if os.path.exists(self.members_file):
                with open(self.members_file, "r") as f:
                    members_data = json.load(f)
                    for member_dict in members_data:
                        member = Member.from_dict(member_dict)
                        self.members[member.member_id] = member
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error loading members from file: {e}")
            print("Starting with empty members list...")
    
    def load_data(self):
        """Load all data from files."""
        self.load_books()
        self.load_members()
    
    # ============ ANALYTICS ============
    
    def get_most_borrowed_book(self):
        """Find and return the most borrowed book."""
        if not self.books:
            return None
        return max(self.books.values(), key=lambda b: b.borrow_count)
    
    def get_currently_borrowed_count(self):
        """Get total number of books currently borrowed."""
        return sum(1 for book in self.books.values() if not book.available)
    
    def get_active_members_count(self):
        """Get total number of active members."""
        return len(self.members)
    
    def get_members_with_books(self):
        """Get members who currently have borrowed books."""
        return [m for m in self.members.values() if m.get_borrowed_count() > 0]
    
    def print_analytics_report(self):
        """Print a comprehensive library analytics report."""
        print("\n" + "=" * 60)
        print("LIBRARY ANALYTICS REPORT".center(60))
        print("=" * 60)
        
        total_books = len(self.books)
        borrowed_books = self.get_currently_borrowed_count()
        available_books = total_books - borrowed_books
        active_members = self.get_active_members_count()
        
        print(f"\n INVENTORY STATUS:")
        print(f"   Total Books in Library: {total_books}")
        print(f"   Books Available: {available_books}")
        print(f"   Books Currently Borrowed: {borrowed_books}")
        print(f"   Availability Rate: {(available_books/total_books*100):.1f}%" if total_books > 0 else "   Availability Rate: N/A")
        
        print(f"\nMEMBER STATISTICS:")
        print(f"   Total Active Members: {active_members}")
        print(f"   Members with Borrowed Books: {len(self.get_members_with_books())}")
        
        print(f"\nMOST BORROWED BOOK:")
        most_borrowed = self.get_most_borrowed_book()
        if most_borrowed:
            print(f"   Title: {most_borrowed.title}")
            print(f"   Author: {most_borrowed.author}")
            print(f"   Times Borrowed: {most_borrowed.borrow_count}")
        else:
            print(f"   No borrow records yet.")
        
        print(f"\nSYSTEM ACTIVITY:")
        print(f"   Total Transactions: {Library.total_transactions}")
        
        print("\n" + "=" * 60 + "\n")
