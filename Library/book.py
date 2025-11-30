"""
Library Book Management System
Author: Vishnu shankar
Assignment: Library Inventory System - Task 2 & 3
Description: Book class for managing book details and availability
"""

class Book:
    """
    Represents a book in the library system.
    
    Attributes:
        title (str): Title of the book
        author (str): Author of the book
        isbn (str): ISBN number (unique identifier)
        available (bool): Availability status (default: True)
    """
    
    def __init__(self, title, author, isbn):
        """
        Initialize a Book instance.
        
        Args:
            title (str): Book title
            author (str): Book author
            isbn (str): ISBN number
        """
        self.title = title
        self.author = author
        self.isbn = isbn
        self.available = True
        self.borrow_count = 0  # Track how many times borrowed
    
    def borrow(self):
        """Mark the book as borrowed (not available)."""
        if self.available:
            self.available = False
            self.borrow_count += 1
            return True
        return False
    
    def return_book(self):
        """Mark the book as returned (available)."""
        if not self.available:
            self.available = True
            return True
        return False
    
    def __str__(self):
        """Return a string representation of the book."""
        status = "Available" if self.available else "Borrowed"
        return f"'{self.title}' by {self.author} (ISBN: {self.isbn}) - {status}"
    
    def __repr__(self):
        """Return a dictionary-like representation for debugging."""
        return f"Book({self.title!r}, {self.author!r}, {self.isbn!r})"
    
    def to_dict(self):
        """Convert book object to dictionary for file storage."""
        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "available": self.available,
            "borrow_count": self.borrow_count
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create a Book instance from a dictionary."""
        book = cls(data["title"], data["author"], data["isbn"])
        book.available = data.get("available", True)
        book.borrow_count = data.get("borrow_count", 0)
        return book
