import pygame as pg
from db.connection import connection

# Класс, описываемый окно самой игры
class MainWindow:
    def __init__(self):
        # Параметры отображения окна
        self.WIDTH = 400
        self.HEIGHT = 400
        self.FPS = 30

        # Задача размеров, цвета, названия окна
        self.screen = pg.display.set_mode((self.WIDTH, self.HEIGHT))
        self.screen.fill((255, 255, 255))
        pg.display.set_caption("Just Click")

        # Инициализация компонентов pygame
        pg.init()
        pg.font.init()
        pg.mixer.init()
        self.clock = pg.time.Clock()

    # Функция для корректного отображения счета на экране
    def add_score(self, player):
        # Задаем настройки шрифта
        myFont = pg.font.SysFont('Comic Sans MS', 30)
        # Заливаем цветом фона прошлый текст (для избежания наложения)
        self.screen.fill(pg.Color("white"), (0, 0, 400, 100))

        # Выводим текущий и лучший счет игрока
        text = myFont.render('Current score: ' + str(player.current_score), False, (0, 0, 0))
        self.screen.blit(text, (10, 10))

        name_text = myFont.render('Best score: ' + str(player.best_score), False, (0, 0, 0))
        self.screen.blit(name_text, (10, 50))

        pg.display.flip()

    # Главная функция запуска игры
    def start_game(self, game_player):
        # Добавляем на экран кнопку
        button = pg.image.load('../res/button.jpg')
        self.button_rect = button.get_rect(center = (self.WIDTH / 2, self.HEIGHT / 2))
        self.screen.blit(button, self.button_rect)
        # Добавляем счет игрока
        self.add_score(game_player)

        # Запускаем основной цикл игры
        running = True
        while running:
            # Ставим счетчик FPS
            self.clock.tick(self.FPS)

            for event in pg.event.get():
                # Если пользователь закрывает окно, то...
                if event.type == pg.QUIT:
                    # Отправляем запрос в БД на сохранение нового лучшего счета
                    conn, cur = connection()
                    cur.execute("""UPDATE users SET score = '""" + str(game_player.best_score) + """'
                                WHERE user_name = '""" + game_player.nickname + """'""")
                    conn.commit()
                    # Завершаем основной цикл игры и выходим
                    running = False
                # При нажатии мыши в область кнопки...
                if event.type == pg.MOUSEBUTTONDOWN and self.button_rect.collidepoint(event.pos):
                    # Увеличиваем текущий счет игрока
                    game_player.current_score += 1
                    if game_player.current_score > game_player.best_score:
                        game_player.best_score = game_player.current_score
                    self.add_score(game_player)


        pg.quit()