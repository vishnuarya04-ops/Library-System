"""
Library Member Management System
Author: Vishnu Shankar
Assignment: Library Inventory System - Task 2
Description: Member class for managing library members and their borrowed books
"""

class Member:
    """
    Represents a library member.
    
    Attributes:
        name (str): Member's full name
        member_id (str): Unique member identifier
        borrowed_books (list): List of ISBN numbers of borrowed books
    """
    
    def __init__(self, name, member_id):
        """
        Initialize a Member instance.
        
        Args:
            name (str): Member's full name
            member_id (str): Unique member identifier
        """
        self.name = name
        self.member_id = member_id
        self.borrowed_books = []
    
    def borrow_book(self, book):
        """
        Add a book to the member's borrowed list.
        
        Args:
            book (Book): Book object to borrow
            
        Returns:
            bool: True if successful, False otherwise
        """
        if book.borrow():
            self.borrowed_books.append(book.isbn)
            return True
        return False
    
    def return_book(self, book):
        """
        Remove a book from the member's borrowed list.
        
        Args:
            book (Book): Book object to return
            
        Returns:
            bool: True if successful, False otherwise
        """
        if book.return_book() and book.isbn in self.borrowed_books:
            self.borrowed_books.remove(book.isbn)
            return True
        return False
    
    def list_books(self):
        """
        Return a list of ISBN numbers of borrowed books.
        
        Returns:
            list: List of ISBNs
        """
        return self.borrowed_books.copy()
    
    def get_borrowed_count(self):
        """Get the number of books currently borrowed."""
        return len(self.borrowed_books)
    
    def __str__(self):
        """Return a string representation of the member."""
        return f"Member: {self.name} (ID: {self.member_id}) - Books Borrowed: {len(self.borrowed_books)}"
    
    def __repr__(self):
        """Return a dictionary-like representation for debugging."""
        return f"Member({self.name!r}, {self.member_id!r})"
    
    def to_dict(self):
        """Convert member object to dictionary for file storage."""
        return {
            "name": self.name,
            "member_id": self.member_id,
            "borrowed_books": self.borrowed_books
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create a Member instance from a dictionary."""
        member = cls(data["name"], data["member_id"])
        member.borrowed_books = data.get("borrowed_books", [])
        return member
