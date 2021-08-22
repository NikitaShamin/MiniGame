from tkinter import *
from functools import partial
from db.connection import connection
from src.classes.player import player
from tkinter import messagebox
from src.classes.MainWindow import MainWindow

# Класс, описывающий форму авторизации
class AuthForm:
    def __init__(self):
        # window - окно авторизации. Далее - настройки отображения окна
        self.window = Tk()
        self.window.title('Just Click')
        self.window.geometry('400x300')
        self.window.resizable(False, False)
        self.nickname = ""

    # Функция, описывающая процесс авторизации
    def authorization(self, username):
        # Считываем с формы имя пользователя
        user_nickname = username.get()
        conn, cur = connection()

        result_player = player()

        # Отправляем запрос в БД, есть ли пользователь с таким именем
        cur.execute("""SELECT EXISTS(SELECT * FROM users WHERE user_name = '""" + user_nickname + """');""")
        result = cur.fetchone()

        # Если нету, то добавляем его в БД
        if (result[0] == 0):
            new_player = player()
            new_player.nickname = user_nickname
            cur.execute("""INSERT INTO users VALUES (?, ?);""", (new_player.nickname, new_player.best_score))
            conn.commit()
            messagebox.showinfo("Success", "Hello, new player!")
            result_player = new_player
        else:
            # Если есть, то считываем с БД его лучший счет и идем дальше
            messagebox.showinfo("Good!", "Hello, old player!")
            cur.execute("""SELECT score FROM users WHERE user_name = '""" + user_nickname + """';""")
            best_score = cur.fetchall()
            result_player.__set__(user_nickname, int(best_score[0][0]), 0)

        # Закрываем окно авторизации
        self.window.destroy()

        # И запускаем саму игру
        main_window = MainWindow()
        main_window.start_game(result_player)

    # Функция для отрисовки самой формы
    def draw_form(self):
        # Описание всех шрифтов и отступов на форме
        font_header = ('Arial', 15)
        font_entry = ('Arial', 12)
        label_font = ('Arial', 11)
        base_padding = {'padx': 10, 'pady': 8}
        header_padding = {'padx': 10, 'pady': 12}

        # Вывод на форму названиий
        main_label = Label(self.window, text='Authorization', font=font_header, justify=CENTER, **header_padding)
        main_label.pack()
        username_label = Label(self.window, text='Nickname', font=label_font, **base_padding)
        username_label.pack()

        # Вывод на форму поля ввода
        username = StringVar()
        username_entry = Entry(self.window, bg='#fff', fg='#444', font=font_entry, textvariable=username)
        username_entry.pack()

        # Вывод на форму кнопку отправки формы
        authorization = partial(self.authorization, username)
        send_btn = Button(self.window, text='Play!', command=authorization)
        send_btn.pack(**base_padding)

        # Запуск окна
        self.window.mainloop()




