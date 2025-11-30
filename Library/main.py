"""
Library Inventory System - Main Interface
Author: Vishnu shankar
Assignment: Library Inventory System - Complete Implementation
Description: Interactive console menu for library management system
"""

from library import Library
import os


def clear_screen():
    """Clear the console screen."""
    os.system("cls" if os.name == "nt" else "clear")

def print_welcome():
    """Print welcome message."""
    print("\n" + "=" * 60)
    print("LIBRARY INVENTORY MANAGEMENT SYSTEM".center(60))
    print("=" * 60)
    print("MCA (AI & ML) - Programming for Problem Solving Using Python")
    print("Assignment 03: OOP-Based Library System")
    print("=" * 60 + "\n")


def display_menu():
    """Display the main menu options."""
    print("\n" + "-" * 60)
    print("MAIN MENU".center(60))
    print("-" * 60)
    print("1. Add a New Book")
    print("2. Register a New Member")
    print("3. Borrow a Book")
    print("4. Return a Book")
    print("5. View All Books")
    print("6. View All Members")
    print("7. View Library Analytics Report")
    print("8. Exit")
    print("-" * 60)


def add_book_menu(library):
    """Menu to add a new book."""
    print("\n--- ADD NEW BOOK ---")
    try:
        title = input("Enter book title: ").strip()
        if not title:
            print(" Error: Title cannot be empty!")
            return
        
        author = input("Enter author name: ").strip()
        if not author:
            print("Error: Author cannot be empty!")
            return
        
        isbn = input("Enter ISBN (unique identifier): ").strip()
        if not isbn:
            print("Error: ISBN cannot be empty!")
            return
        
        if library.add_book(title, author, isbn):
            print(f"Book '{title}' added successfully!")
        else:
            print(f"Error: Book with ISBN '{isbn}' already exists!")
    except Exception as e:
        print(f" Error: {e}")


def register_member_menu(library):
    """Menu to register a new member."""
    print("\n--- REGISTER NEW MEMBER ---")
    try:
        name = input("Enter member name: ").strip()
        if not name:
            print("Error: Name cannot be empty!")
            return
        
        member_id = input("Enter member ID (unique): ").strip()
        if not member_id:
            print("Error: Member ID cannot be empty!")
            return
        
        if library.register_member(name, member_id):
            print(f"Member '{name}' registered successfully!")
        else:
            print(f"Error: Member ID '{member_id}' already exists!")
    except Exception as e:
        print(f" Error: {e}")


def borrow_book_menu(library):
    """Menu to borrow a book."""
    print("\n--- BORROW A BOOK ---")
    try:
        member_id = input("Enter member ID: ").strip()
        isbn = input("Enter book ISBN: ").strip()
        
        if not member_id or not isbn:
            print("Error: Member ID and ISBN cannot be empty!")
            return
        
        member = library.get_member_by_id(member_id)
        book = library.get_book_by_isbn(isbn)
        
        if not member:
            print(f"Error: Member ID '{member_id}' not found!")
            return
        if not book:
            print(f"Error: Book with ISBN '{isbn}' not found!")
            return
        
        if library.lend_book(member_id, isbn):
            print(f"'{book.title}' borrowed successfully by {member.name}!")
        else:
            print(f"Failed to borrow book!")
    except Exception as e:
        print(f" Error: {e}")


def return_book_menu(library):
    """Menu to return a book."""
    print("\n--- RETURN A BOOK ---")
    try:
        member_id = input("Enter member ID: ").strip()
        isbn = input("Enter book ISBN: ").strip()
        
        if not member_id or not isbn:
            print("Error: Member ID and ISBN cannot be empty!")
            return
        
        member = library.get_member_by_id(member_id)
        book = library.get_book_by_isbn(isbn)
        
        if not member:
            print(f"Error: Member ID '{member_id}' not found!")
            return
        if not book:
            print(f"Error: Book with ISBN '{isbn}' not found!")
            return
        
        if library.take_return(member_id, isbn):
            print(f"'{book.title}' returned successfully by {member.name}!")
        else:
            print(f"Failed to return book!")
    except Exception as e:
        print(f" Error: {e}")


def view_all_books(library):
    """Display all books in the library."""
    print("\n--- ALL BOOKS IN LIBRARY ---")
    books = library.list_all_books()
    
    if not books:
        print(" No books in the library yet.")
    else:
        print(f"\nTotal Books: {len(books)}\n")
        for idx, book in enumerate(books, 1):
            print(f"{idx}. {book}")
    print()


def view_all_members(library):
    """Display all registered members."""
    print("\n--- ALL REGISTERED MEMBERS ---")
    members = library.list_all_members()
    
    if not members:
        print("No members registered yet.")
    else:
        print(f"\nTotal Members: {len(members)}\n")
        for idx, member in enumerate(members, 1):
            print(f"{idx}. {member}")
            borrowed = member.list_books()
            if borrowed:
                print(f"Borrowed ISBNs: {', '.join(borrowed)}")
    print()


def main():
    """Main function to run the library system."""
    clear_screen()
    print_welcome()
    
    # Initialize the library system
    library = Library()
    
    # Main loop
    while True:
        display_menu()
        choice = input("Select an option (1-8): ").strip()
        
        if choice == "1":
            add_book_menu(library)
        elif choice == "2":
            register_member_menu(library)
        elif choice == "3":
            borrow_book_menu(library)
        elif choice == "4":
            return_book_menu(library)
        elif choice == "5":
            view_all_books(library)
        elif choice == "6":
            view_all_members(library)
        elif choice == "7":
            library.print_analytics_report()
        elif choice == "8":
            print("\nThank you for using Library Inventory System!")
            print("Data has been saved automatically.\n")
            break
        else:
            print("Invalid option! Please select 1-8.")


if __name__ == "__main__":
    main()
