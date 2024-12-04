import json
from enum import Enum
from typing import List, Dict, Optional

# Путь к файлу с данными
DATA_FILE = "data/books.json"


class BookStatus(Enum):
    AVAILABLE = "в наличии"
    ISSUED = "выдана"


class Book:
    def __init__(
        self, book_id: int,
        title: str,
        author: str,
        year: int,
        status: BookStatus = BookStatus.AVAILABLE
    ):
        self.id = book_id
        self.title = title
        self.author = author
        self.year = year
        self.status = BookStatus(status) if isinstance(status, str) else status

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status.value
        }

    @staticmethod
    def from_dict(data: Dict):
        return Book(
            data["id"],
            data["title"],
            data["author"],
            data["year"],
            data["status"]
        )


class Library:
    def __init__(self):
        self.books = self.load_books()

    @staticmethod
    def load_books() -> List[Book]:
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)
                return [Book.from_dict(book) for book in data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_books(self):
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump([book.to_dict() for book in self.books], file, ensure_ascii=False, indent=4)

    def add_book(self, title: str, author: str, year: int):
        new_id = max((book.id for book in self.books), default=0) + 1
        new_book = Book(new_id, title, author, year)
        self.books.append(new_book)
        self.save_books()

    def delete_book(self, book_id: int) -> bool:
        for book in self.books:
            if book.id == book_id:
                self.books.remove(book)
                self.save_books()
                return True
        return False

    def search_books(self, query: str, field: str) -> List[Book]:
        field_map = {
            "название": lambda b: b.title,
            "автор": lambda b: b.author,
            "год": lambda b: str(b.year)
        }
        if field not in field_map:
            raise ValueError("Некорректное поле для поиска.")
        return [book for book in self.books if query.lower() in field_map[field](book).lower()]

    def list_books(self) -> List[Book]:
        return self.books

    def update_status(self, book_id: int, status: str) -> bool:
        try:
            new_status = BookStatus(status)
        except ValueError:
            return False
        for book in self.books:
            if book.id == book_id:
                book.status = new_status
                self.save_books()
                return True
        return False
