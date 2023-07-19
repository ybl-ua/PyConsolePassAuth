from database_functional import *


class UnsignedUser:
    def __init__(self):
        pass

    # Функція авторизації
    def auth(self):
        clear()
        attempt_counter = 0
        while attempt_counter < 3:
            print('----------Авторизація----------')
            login = input('Введіть логін: ')
            password = stdiomask.getpass('Введіть пароль: ')
            account = user_is_exist(login, password)
            if account and not account[2]:
                return SignedUser(account)
            elif account and account[2]:
                return Admin(account)
            attempt_counter += 1
        exit()  # Завершення програми при 3х невдалих спробах входу

    # Створення нового облікового запису
    def sign_up(self):
        clear()
        print('Меню створення нового облікового запису.')
        # Цикл, що переривається після успішного вводу всіх данних
        while True:
            login = input('Введіть логін: ')
            # Цикл для перевірки паролю
            while True:
                password = stdiomask.getpass('Введіть пароль: ')
                if password == stdiomask.getpass('Підтвердіть пароль: '):
                    if password_is_secure(password):
                        break
                    else:
                        clear()
                        print('''Пароль недостатньо надійний.\nБезпечний пароль повинен складатись з літер, цифр та розділових знаків\n''')
                else:
                    clear()
                    print('Паролі не сходяться')
            if add_user_to_database(login, password, False, False, True):
                break

    # Функція виведення інформації про програму
    def about(self):
        clear()
        print('----------Інформація про програму----------')
        print('Автор програми: ст. гр. 125-19-1 Іванов С.С.')
        print('Варіант 9: Наявність букв, цифр і розділових знаків.')
        input('\nНатисніть Enter, щоб повернутись.')

    # Відображення меню неідинтифікованого користувача
    def menu(self):
        while True:
            clear()
            print('Привіт, вам необхідно увійти до аккаунту або створити новий!\n')
            print('[1] Авторизація')
            print('[2] Реєстрація')
            print('[3] Про програму')
            print('[4] Завершити роботу\n')
            option = input('Оберіть опцію: ')
            if option == '1':
                return self.auth()
            elif option == '2':
                self.sign_up()
            elif option == '3':
                self.about()
            elif option == '4':
                exit()


class SignedUser:
    def __init__(self, account):
        self.name = account[0]
        self.__password = account[1]
        self.adminstatus = account[2]
        self.banned = account[3]
        self.password_limit = account[4]
        if self.banned:
            input('Аккаунт заблоковано! Натисніть Enter для продовження')
            exit()

    # Метод зміни паролю
    def change_password(self):
        clear()
        # Перевірки необхідних вимог(надійність пароля, правильність вводу, аутентифікація користувача)
        while True:
            if self.__password == stdiomask.getpass('Введіть пароль: '):
                while True:
                    new_password = stdiomask.getpass('Введіть новий пароль: ')
                    if new_password == stdiomask.getpass('Повторіть новий пароль: '):
                        if not self.password_limit or password_is_secure(new_password):
                            self.__password = new_password
                            break
                        else:
                            clear()
                            print('Пароль недостатньо найдійний!')
                    else:
                        clear()
                        print('Паролі не сходяться')
                update_db(self.name, self.__password)
                print('Пароль змінено!')
                break
            else:
                print('Пароль не вірний! Повторіть спробу')

    # Функція виведення інформації про програму
    def about(self):
        clear()
        print('----------Інформація про програму----------')
        print('Автор програми: ст. гр. 125-19-1 Іванов С.С.')
        print('Варіант 9: Наявність букв, цифр і розділових знаків.')
        input('\nНатисніть Enter, щоб повернутись.')

    # Відображення меню звичайного користувача
    def menu(self):
        while True:
            clear()
            print(f'Привіт, {self.name}\n')
            print('[1] Змінити пароль')
            print('[2] Про програму')
            print('[3] Завершити роботу\n')
            option = input('Оберіть опцію: ')
            if option == '1':
                self.change_password()
            elif option == '2':
                self.about()
            elif option == '3':
                exit()


class Admin(SignedUser):
    # Метод перегляду списку користувачів
    def check_list_users(self):
        clear()
        print('Оберіть опцію\n')
        print('[1] Переглянути весь список')
        print('[2] Переглянути по одному')
        print('[3] Повернутися в меню')
        option = input('Опція:')
        clear()
        # Перша опція дає можливість переглянути відразу весь список
        if option == '1':
            user_list = [i for i in bd_get_usernames()]
            counter = 1
            for user in user_list:
                print(f'{counter}) Логін: {user[0]}\t\tПрава адміністратора: {bool(user[1])}\tБан: {bool(user[2])}\tОбмеження паролю: {bool(user[3])}')
                counter += 1
            input('\nНажміть Enter, щоб повернутися в меню')
        # Друга опція дає можливість переглянути користувачів по одному
        elif option == '2':
            user_list = [i for i in bd_get_usernames()]
            for i in range(len(user_list)):
                user_list[i] = f'{i+1}) Логін: {user_list[i][0]}\t\tПрава адміністратора: {bool(user_list[i][1])}\tБан: {bool(user_list[i][2])}\tОбмеження паролю: {bool(user_list[i][3])}'

            counter = 0
            # Меню переміщення по списку користувачів
            while True:
                counter %= len(user_list)
                print(user_list[counter])
                print('\n[1] Переглянути наступного користувача')
                print('[2] Переглянути попередньго користувача')
                print('[3] Повернутися на початок списку')
                print('[4] Перейти в кінець списку')
                print('[5] Повернутися в меню\n')
                option = input('Оберіть опцію: ')
                clear()
                if option == '1':
                    counter += 1
                elif option == '2':
                    counter -= 1
                elif option == '3':
                    counter = 0
                elif option == '4':
                    counter = len(user_list) - 1
                elif option == '5':
                    break
        # Третя опція виходить з меню перегляду користувачів
        elif option == '3':
            return None

    # Метод створення нового користувача з порожнім паролем
    def add_new_user(self):
        clear()
        # Викликається функція створення нового користувача в бд, створюється юзер з базовими правами та пустим паролем
        while True:
            print('----------Створення нового користувача----------')
            print("------------Паролем буде пустий рядок-----------\n")
            login = input("Введіть ім'я нового користувача: ")
            if add_user_to_database(login, '', False, False, True):
                break
            else:
                clear()
                print('Логін вже використовується. Спробуйте ще раз')

    # Метод блокування користувачів
    def ban_user(self):
        # Меню блокування\розблокування користувача
        while True:
            clear()
            print("----------Блокування користувача----------")
            print('\n[1] Заблокувати користувача')
            print('[2] Розблокувати користувача')
            print('[3] Повернутися в меню\n')
            option = input('Оберіть опцію: ')
            clear()
            # Відповідно до обраної опції змінюється параметр в бд
            if option == '1':
                login = input("Введіть ім'я користувача: ")
                bd_ban_user(login, True)
            elif option == '2':
                login = input("Введіть ім'я користувача: ")
                bd_ban_user(login, False)
            elif option == '3':
                break

    # Метод зміни налаштуваннь паролів користувачів
    def change_user_password_setting(self):
        # Меню зміни налаштуваннь пароля користувача
        while True:
            clear()
            print("----------Зміна налаштувань паролю користувача----------")
            print('\n[1] Увімкнути обмеження паролю користувача')
            print('[2] Вимкнути обмеження паролю користувача')
            print('[3] Повернутися в меню\n')
            option = input('Оберіть опцію: ')
            clear()
            # Відповідно до обраної опції змінюється параметр в бд
            if option == '1':
                login = input("Введіть ім'я користувача: ")
                bd_change_password_setting(login, True)
            elif option == '2':
                login = input("Введіть ім'я користувача: ")
                bd_change_password_setting(login, False)
            elif option == '3':
                break

    # Відображення меню адміністратора
    def menu(self):
        while True:
            clear()
            print(f'Привіт, {self.name}\n')
            print('[1] Змінити пароль')
            print('[2] Переглянути список користувачів')
            print('[3] Створити нового користувача')
            print('[4] Блокування користувачів')
            print('[5] Налаштування паролів користувачів')
            print('[6] Про програму')
            print('[7] Завершити роботу\n')
            option = input('Оберіть опцію: ')
            if option == '1':
                self.change_password()
            elif option == '2':
                self.check_list_users()
            elif option == '3':
                self.add_new_user()
            elif option == '4':
                self.ban_user()
            elif option == '5':
                self.change_user_password_setting()
            elif option == '5':
                self.about()
            elif option == '7':
                exit()


if __name__ == '__main__':
    user = UnsignedUser()
    while True:
        user = user.menu()
