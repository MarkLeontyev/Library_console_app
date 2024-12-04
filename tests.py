import unittest
import os
from library import Book, Library

DATA_FILE_FOR_TEST = "data/books_test.json"


class TestLibrary(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Создаём временную библиотеку один раз для всего класса."""
        cls.library = Library()
        cls.test_data = [
            Book(1, "Преступление и наказание", "Ф. М. Достоевский", 1866),
            Book(2, "Мастер и Маргарита", "М. А. Булгаков", 1940),
            Book(3, "Идиот", "Ф. М. Достоевский", 1869)
        ]
        cls.library.books = cls.test_data

    @classmethod
    def tearDownClass(cls):
        """
        Удаляем временный файл данных один раз
        после выполнения всех тестов.
        """
        if os.path.exists(DATA_FILE_FOR_TEST):
            os.remove(DATA_FILE_FOR_TEST)

    def test_add_book(self):
        """Тест добавления книги в библиотеку."""
        self.library.add_book("Тихий Дон", "М. А. Шолохов", 1928)
        self.assertEqual(len(self.library.books), 4)
        self.assertEqual(self.library.books[-1].title, "Тихий Дон")
        self.assertEqual(self.library.books[-1].author, "М. А. Шолохов")
        self.assertEqual(self.library.books[-1].year, 1928)

    def test_delete_nonexistent_book(self):
        """Тест удаления несуществующей книги."""
        self.assertFalse(self.library.delete_book(99))

    def test_search_books_by_title(self):
        """Тест поиска книги по названию."""
        results = self.library.search_books("Преступление", "название")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Преступление и наказание")

    def test_search_books_by_author(self):
        """Тест поиска книги по автору."""
        results = self.library.search_books("Достоевский", "автор")
        self.assertEqual(len(results), 2)

    def test_search_books_by_year(self):
        """Тест поиска книги по году."""
        results = self.library.search_books("1940", "год")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Мастер и Маргарита")

    def test_search_books_invalid_field(self):
        """Тест поиска по некорректному полю."""
        with self.assertRaises(ValueError):
            self.library.search_books("Тихий Дон", "genre")

    def test_list_books(self):
        """Тест получения списка всех книг."""
        books = self.library.list_books()
        self.assertEqual(len(books), 3)
        self.assertEqual(books[0].title, "Преступление и наказание")

    def test_update_status(self):
        """Тест обновления статуса книги."""
        self.assertTrue(self.library.update_status(1, "выдана"))
        self.assertEqual(self.library.books[0].status, "выдана")

    def test_update_status_invalid(self):
        """Тест обновления статуса несуществующей книги."""
        self.assertFalse(self.library.update_status(99, "выдана"))

    def test_update_status_invalid_status(self):
        """Тест обновления статуса с некорректным значением."""
        self.assertFalse(self.library.update_status(1, "потеряна"))

    def test_save_and_load_books(self):
        """Тест сохранения и загрузки книг."""
        self.library.save_books()
        loaded_library = Library()
        self.assertEqual(len(loaded_library.books), 3)
        self.assertEqual(
            loaded_library.books[0].title, "Преступление и наказание"
        )

    def test_delete_book(self):
        """Тест удаления книги из библиотеки."""
        self.assertTrue(self.library.delete_book(2))
        self.assertEqual(len(self.library.books), 3)
        self.assertFalse(any(book.id == 2 for book in self.library.books))


if __name__ == "__main__":
    unittest.main()
