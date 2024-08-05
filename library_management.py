import csv
from datetime import datetime

# Book class
class Book:
    def __init__(self, title, author, isbn, publication_date, available=True):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.publication_date = publication_date
        self.available = available

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "publication_date": self.publication_date,
            "available": self.available
        }


# Member class
class Member:
    def __init__(self, member_id, name, contact_info):
        self.member_id = member_id
        self.name = name
        self.contact_info = contact_info

    def to_dict(self):
        return {
            "member_id": self.member_id,
            "name": self.name,
            "contact_info": self.contact_info
        }


class Library:
    def __init__(self, books_file='books.csv', members_file='members.csv'):
        self.books_file = books_file
        self.members_file = members_file
        self.books = self.load_books()
        self.members = self.load_members()

    def load_books(self):
        books = []
        try:
            with open(self.books_file, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    book = Book(
                        title=row["title"],
                        author=row["author"],
                        isbn=row["isbn"],
                        publication_date=row["publication_date"],
                        available=row["available"] == 'True'
                    )
                    books.append(book)
        except FileNotFoundError:
            pass
        return books

    def load_members(self):
        members = []
        try:
            with open(self.members_file, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    member = Member(
                        member_id=row["member_id"],
                        name=row["name"],
                        contact_info=row["contact_info"]
                    )
                    members.append(member)
        except FileNotFoundError:
            pass
        return members

    def save_books(self):
        with open(self.books_file, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["title", "author", "isbn", "publication_date", "available"])
            writer.writeheader()
            for book in self.books:
                writer.writerow(book.to_dict())

    def save_members(self):
        with open(self.members_file, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["member_id", "name", "contact_info"])
            writer.writeheader()
            for member in self.members:
                writer.writerow(member.to_dict())

    def add_book(self, book):
        self.books.append(book)
        self.save_books()

    def display_books(self):
        for book in self.books:
            print(f"Title: {book.title}, Author: {book.author}, ISBN: {book.isbn}, Published: {book.publication_date}, Available: {book.available}")

    def search_book(self, search_term):
        results = [book for book in self.books if search_term.lower() in book.title.lower() or search_term.lower() in book.isbn.lower()]
        return results

    def remove_book(self, search_term):
        self.books = [book for book in self.books if search_term.lower() not in book.title.lower() and search_term.lower() not in book.isbn.lower()]
        self.save_books()

    def add_member(self, member):
        self.members.append(member)
        self.save_members()


class Transaction:
    def __init__(self, book_isbn, member_id, issue_date, return_date=None, fine=0):
        self.book_isbn = book_isbn
        self.member_id = member_id
        self.issue_date = issue_date
        self.return_date = return_date
        self.fine = fine

    def to_dict(self):
        return {
            "book_isbn": self.book_isbn,
            "member_id": self.member_id,
            "issue_date": self.issue_date,
            "return_date": self.return_date,
            "fine": self.fine
        }


class LibraryManagementSystem(Library):
    def __init__(self, books_file='books.csv', members_file='members.csv', transactions_file='transactions.csv'):
        super().__init__(books_file, members_file)
        self.transactions_file = transactions_file
        self.transactions = self.load_transactions()

    def load_transactions(self):
        transactions = []
        try:
            with open(self.transactions_file, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    transaction = Transaction(
                        book_isbn=row["book_isbn"],
                        member_id=row["member_id"],
                        issue_date=row["issue_date"],
                        return_date=row["return_date"] if row["return_date"] else None,
                        fine=float(row["fine"])
                    )
                    transactions.append(transaction)
        except FileNotFoundError:
            pass
        return transactions

    def save_transactions(self):
        with open(self.transactions_file, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["book_isbn", "member_id", "issue_date", "return_date", "fine"])
            writer.writeheader()
            for transaction in self.transactions:
                writer.writerow(transaction.to_dict())

    def issue_book(self, book_isbn, member_id):
        for book in self.books:
            if book.isbn == book_isbn and book.available:
                book.available = False
                self.save_books()
                transaction = Transaction(book_isbn, member_id, datetime.now().strftime("%Y-%m-%d"))
                self.transactions.append(transaction)
                self.save_transactions()
                return f"Book '{book.title}' issued to member ID {member_id}"
        return "Book not available or not found"

    def return_book(self, book_isbn, member_id):
        for transaction in self.transactions:
            if transaction.book_isbn == book_isbn and transaction.member_id == member_id and not transaction.return_date:
                transaction.return_date = datetime.now().strftime("%Y-%m-%d")
                issue_date = datetime.strptime(transaction.issue_date, "%Y-%m-%d")
                return_date = datetime.strptime(transaction.return_date, "%Y-%m-%d")
                days_overdue = (return_date - issue_date).days - 14  # Assuming a 14-day loan period
                if days_overdue > 0:
                    transaction.fine = days_overdue * 1  # Assuming $1 per day overdue
                self.save_transactions()
                for book in self.books:
                    if book.isbn == book_isbn:
                        book.available = True
                        self.save_books()
                        return f"Book '{book.title}' returned by member ID {member_id} with fine: ${transaction.fine}"
        return "Transaction not found"

    def generate_report(self):
        report = {
            "total_books": len(self.books),
            "issued_books": len([transaction for transaction in self.transactions if not transaction.return_date]),
            "members": len(self.members),
            "transactions": len(self.transactions)
        }
        return report
