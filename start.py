from user_functional import *


if __name__ == '__main__':
    create_users_database()  # Створення бази даних користувачів
    user = UnsignedUser()    # Створення класу неавторизованного користувача
    while True:
        user = user.menu()  # Відображення меню відповідно до класу
