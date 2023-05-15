import tkinter as tk


class MyButton(tk.Button):
    def __init__(self, master, x, y, number, *args, **kwargs):
        super(MyButton, self).__init__(master, width=3, height=3, font='Calibri 15 bold', *args, **kwargs)
        self.x = x  # координаты
        self.y = y
        self.is_mine = False  # стоит ли тут мина
        self.number = number  # порядковый номер кнопки на поле
        self.mine_around = 0  # мин вокруг
        self.is_open = False  # нажата ли кнопка

        self.color = 'black'  # цвет символа при нажатии кнопки

        self.colors = {
            0: 'black',
            1: 'Blue',
            2: 'Green',
            3: 'Red',
            4: 'Purple',
            5: 'Orange',
            6: 'Blue',
            7: 'Pink',
            8: 'Brown'
        }

    def __repr__(self):
        return f'{self.number}: ({self.x}.{self.y}) - {self.is_mine} {self.mine_around}'

    def foreground(self):
        self.color = self.colors[self.mine_around]
