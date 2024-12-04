from library import Library


def main():
    library = Library()
    while True:
        print("\nУправление библиотекой:")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Искать книгу")
        print("4. Показать все книги")
        print("5. Изменить статус книги")
        print("0. Выход")
        choice = input("Выберите действие: ")
        try:
            if choice == "1":
                title = input("Введите название книги: ")
                author = input("Введите автора: ")
                year = int(input("Введите год издания: "))
                library.add_book(title, author, year)
                print("Книга добавлена.")
            elif choice == "2":
                book_id = int(input("Введите ID книги для удаления: "))
                if library.delete_book(book_id):
                    print("Книга удалена.")
                else:
                    print("Книга с таким ID не найдена.")
            elif choice == "3":
                field = input("Искать по (название/автор/год): ").strip()
                query = input("Введите значение для поиска: ")
                results = library.search_books(query, field)
                if results:
                    print("\nНайденные книги:")
                    for book in results:
                        print(f"ID книги: {book.id}, название: \"{book.title}\" написанная автором: {book.author} в: {book.year} году в данный момент {book.status.value}")
                else:
                    print("Книги не найдены.")
            elif choice == "4":
                books = library.list_books()
                for book in books:
                    print(f"ID книги: {book.id}, название: \"{book.title}\" написанная автором: {book.author} в: {book.year} году в данный момент {book.status.value}")
            elif choice == "5":
                book_id = int(input("Введите ID книги: "))
                status = input("Введите новый статус (в наличии/выдана): ").strip()
                if library.update_status(book_id, status):
                    print("Статус обновлен.")
                else:
                    print("Такого статуса не существет.")
            elif choice == "0":
                print("До свидания!")
                break
            else:
                print("Некорректный выбор.")
        except ValueError as e:
            print(f"Ошибка ввода: {e}")

if __name__ == "__main__":
    main()
