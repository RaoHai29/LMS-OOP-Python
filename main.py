from library_management import LibraryManagementSystem, Book, Member

def main():
    # Welcome screen
    print("#################################################################")
    print("Welcome to Library Management System")
    print("Designed by:")
    print("RAO ABDUL HAI | WEB DEVELOPER | PYTHON PROGRAM USING OOP | DUET")
    print("#################################################################")

    
    proceed = input("\nPress 'y' to continue: ").strip().lower()
    if proceed != 'y':
        print("Exiting the system.")
        return

    # Initialize the Library Management System
    lms = LibraryManagementSystem()

    while True:
        print("#################################################################")
        print("\nLibrary Management System")
        print("1. Add Book")
        print("2. Display Books")
        print("3. Search Book")
        print("4. Remove Book")
        print("5. Add Member")
        print("6. Issue Book")
        print("7. Return Book")
        print("8. Generate Report")
        print("9. Exit")
        print("#################################################################")

        choice = input("Enter your choice: ")

        if choice == '1':
            title = input("Enter book title: ")
            author = input("Enter book author: ")
            isbn = input("Enter book ISBN: ")
            publication_date = input("Enter book publication date (YYYY-MM-DD): ")
            book = Book(title, author, isbn, publication_date)
            lms.add_book(book)
            print("Book added successfully.")

        elif choice == '2':
            print("\nDisplaying all books:")
            lms.display_books()

        elif choice == '3':
            search_term = input("Enter book title or ISBN to search: ")
            results = lms.search_book(search_term)
            if results:
                for book in results:
                    print(f"Found Book: Title: {book.title}, Author: {book.author}, ISBN: {book.isbn}")
            else:
                print("No matching books found.")

        elif choice == '4':
            search_term = input("Enter book title or ISBN to remove: ")
            lms.remove_book(search_term)
            print("Book removed successfully.")

        elif choice == '5':
            member_id = input("Enter member ID: ")
            name = input("Enter member name: ")
            contact_info = input("Enter member contact info: ")
            member = Member(member_id, name, contact_info)
            lms.add_member(member)
            print("Member added successfully.")

        elif choice == '6':
            book_isbn = input("Enter book ISBN to issue: ")
            member_id = input("Enter member ID: ")
            print(lms.issue_book(book_isbn, member_id))

        elif choice == '7':
            book_isbn = input("Enter book ISBN to return: ")
            member_id = input("Enter member ID: ")
            print(lms.return_book(book_isbn, member_id))

        elif choice == '8':
            report = lms.generate_report()
            print(f"Report: {report}")

        elif choice == '9':
            print("Exiting the system.")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
