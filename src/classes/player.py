# Класс, описывающий игрока
class player:
    def __init__(self):
        self.nickname = ""
        self.best_score = 0
        self.current_score = 0

    def __get__(self):
        return [self.nickname, self.best_score, self.current_score]

    def __set__(self, name, best_score, score):
        (self.nickname, self.best_score, self.current_score) = (name, best_score, score)

