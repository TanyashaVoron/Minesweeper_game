from random import shuffle

from Button import MyButton


class Field:
    def __init__(self):
        self.row = 10  # кол-во рядов на поле
        self.columns = 10  # кол-во колонок на поле
        self.mines = 10  # кол-во мин на поле
        self.buttons = []

    def not_mines(self):
        """
        проверка на выйгрыш
        """
        for row in self.buttons:
            for line in row:
                if not line.is_mine and not line.is_open:
                    return False
        return True

    def bfs(self, button: MyButton):
        """
        обход кнопок в ширину для раскрытия соседних пустых клеток
        :param button: стартовая ячейка
        """
        queue = [button]
        visited = [button]
        while queue:
            cur_button = queue.pop()
            button.is_open = True
            visited.append(button)

            if cur_button.mine_around != 0:
                cur_button.config(text=cur_button.mine_around, bg='gray', disabledforeground=cur_button.color)
            else:
                cur_button.config(text='', bg='gray', disabledforeground=cur_button.color)
            cur_button.config(state='disabled')
            cur_button.is_open = True

            if cur_button.mine_around == 0:
                x, y = cur_button.x, cur_button.y
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if self.field_limitation(x + dx, y + dy):
                            next_btn = self.next_button(x + dx, y + dy)
                            if not next_btn.is_open and next_btn not in visited:
                                queue.append(next_btn)
                                visited.append(next_btn)

    def field_limitation(self, x, y):
        return 0 <= x < self.row and 0 <= y < self.columns

    def next_button(self, x, y):
        return self.buttons[x][y]

    def get_mines_places(self, clicked_button_numbers):
        """
        индексы мин
        """
        indexes = list(range(1, self.columns * self.row + 1))
        indexes.remove(clicked_button_numbers)
        shuffle(indexes)
        return indexes[:self.mines]

    def insert_mines(self, clicked_button_numbers):
        """
        обозначаем кнопки минами
        выбор мин: (кнопки в масс) - (перемешать) - (взять первуе Н штук) - (список мин)
        """

        index_mines = self.get_mines_places(clicked_button_numbers)
        for row_button in self.buttons:
            for button in row_button:
                if button.number in index_mines:
                    button.is_mine = True
        self.counting_mines()

    def count_mines_around(self, button):
        """
        ищем мины вокруг
        """
        count_mines = 0
        x, y = button.x, button.y
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if self.field_limitation(x + dx, y + dy):
                    if self.next_button(x + dx, y + dy).is_mine:
                        count_mines += 1
        return count_mines

    def counting_mines(self):
        """
        помечаем поля без мин количеством мин вокруг
        """
        for row_button in self.buttons:
            for button in row_button:
                if not button.is_mine:
                    button.mine_around = self.count_mines_around(button)
                    button.foreground()

    def restart_field(self):
        for i in range(self.row):
            for j in range(self.columns):
                btn = self.buttons[i][j]
                if btn.is_mine:
                    btn.config(text='*')
