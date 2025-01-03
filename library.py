import json
import os
from enum import Enum
from typing import Dict, List

# Путь к файлу с данными
DATA_FILE = "data/books.json"


class BookStatus(Enum):
    """Статусы книги."""
    AVAILABLE = "в наличии"
    ISSUED = "выдана"


class Book:
    """Модель книги с атрибутами и методами для преобразования данных."""

    def __init__(
        self, book_id: int,
        title: str,
        author: str,
        year: int,
        status: BookStatus = BookStatus.AVAILABLE
    ):
        """Инициализация книги."""
        self.id = book_id
        self.title = title
        self.author = author
        self.year = year
        self.status = BookStatus(status) if isinstance(status, str) else status

    def to_dict(self) -> Dict:
        """Преобразует объект книги в словарь."""
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status.value
        }

    @staticmethod
    def from_dict(data: Dict):
        """Создаёт объект книги из словаря."""
        return Book(
            data["id"],
            data["title"],
            data["author"],
            data["year"],
            data["status"]
        )


class Library:
    """Библиотека для управления коллекцией книг."""

    def __init__(self, data_file: str = DATA_FILE):
        """Инициализация библиотеки с загрузкой данных из файла."""
        self.data_file = data_file
        self.ensure_data_file_exists()
        self.books = self.load_books()

    def ensure_data_file_exists(self):
        """
        Проверяет существование файла данных и создаёт его,
        если он отсутствует.
        """
        if not os.path.exists(self.data_file):
            with open(self.data_file, "w", encoding="utf-8") as file:
                json.dump([], file, ensure_ascii=False, indent=4)

    def load_books(self) -> List[Book]:
        """Загружает книги из файла данных."""
        try:
            with open(self.data_file, "r", encoding="utf-8") as file:
                data = json.load(file)
                return [Book.from_dict(book) for book in data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_books(self):
        """Сохраняет список книг в файл данных."""
        with open(self.data_file, "w", encoding="utf-8") as file:
            json.dump(
                [book.to_dict() for book in self.books],
                file,
                ensure_ascii=False,
                indent=4
            )

    def add_book(self, title: str, author: str, year: int):
        """Добавляет новую книгу в библиотеку."""
        new_id = max((book.id for book in self.books), default=0) + 1
        new_book = Book(new_id, title, author, year)
        self.books.append(new_book)
        self.save_books()

    def delete_book(self, book_id: int) -> bool:
        """Удаляет книгу по её идентификатору."""
        for book in self.books:
            if book.id == book_id:
                self.books.remove(book)
                self.save_books()
                return True
        return False

    def search_books(self, query: str, field: str) -> List[Book]:
        """Ищет книги по заданному полю и строке запроса."""
        field_map = {
            "название": lambda b: b.title,
            "автор": lambda b: b.author,
            "год": lambda b: str(b.year)
        }
        if field not in field_map:
            raise ValueError("Некорректное поле для поиска.")
        found_books = [
            book for book in self.books
            if query.lower() in field_map[field](book).lower()
        ]
        return found_books

    def list_books(self) -> List[Book]:
        """Возвращает список всех книг в библиотеке."""
        return self.books

    def update_status(self, book_id: int, status: str) -> bool:
        """Обновляет статус книги по её идентификатору."""
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
