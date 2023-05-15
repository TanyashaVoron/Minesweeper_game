import tkinter as tk
from random import shuffle
from tkinter.messagebox import showinfo, showerror

from Button import MyButton


class MineSweeper:
    window = tk.Tk()  # основное окно игры
    ROW = 10  # кол-во рядов на поле
    COLUMNS = 10  # кол-во колонок на поле
    MINES = 10  # кол-во мин на поле
    IS_GAME_OVER = False  # флаг конца игры
    IS_FIRST_CLICK = True  # флаг первого клика игры

    def __init__(self):

        self.window.wm_title('Sapper')
        self.buttons = []
        count = 1
        for i in range(MineSweeper.ROW):
            temp = []
            for j in range(MineSweeper.COLUMNS):
                btn = MyButton(MineSweeper.window, x=i, y=j, number=count)
                btn.config(command=lambda button=btn: self.click(button))  # обработка нажатия левой кнопки мыши
                btn.bind("<Button-3>", self.right_click)  # обработка нажатия правой кнопки мыши
                temp.append(btn)
                count += 1
            self.buttons.append(temp)

    # обработка щелчка правой кнопки мыши (постановка флажка)
    def right_click(self, event):
        if MineSweeper.IS_GAME_OVER:
            return
        cur_btn = event.widget
        if cur_btn['state'] == 'normal':
            cur_btn['state'] = 'disabled'
            cur_btn['text'] = '&'
            cur_btn['disabledforeground'] = 'red'
        elif cur_btn['text'] == '&':
            cur_btn['text'] = ''
            cur_btn['state'] = 'normal'

    # обработка конца игры
    def game_over(self):
        MineSweeper.IS_GAME_OVER = True
        showinfo('Game over', 'Вы проиграли(')
        for i in range(MineSweeper.ROW):
            for j in range(MineSweeper.COLUMNS):
                btn = self.buttons[i][j]
                if btn.is_mine:
                    btn.config(text='*')

    # обход кнопок в ширину для раскрытия радом с пустыми клетками
    def bfs(self, button: MyButton):
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

            if cur_button.mine_around == 0:
                x, y = cur_button.x, cur_button.y
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:

                        if 0 <= x + dx < MineSweeper.ROW and 0 <= y + dy < MineSweeper.COLUMNS:
                            next_btn = self.buttons[x + dx][y + dy]
                            if not next_btn.is_open and next_btn not in visited:
                                queue.append(next_btn)
                                visited.append(next_btn)

    # реакция на нажатие кнопки. Почему сюда, а не в кнопку?
    # тк при нажатии реакция должна проходить не только на саму кнопку
    # но еще и на соседние(если они пустые)
    def click(self, clicked_button: MyButton):

        if MineSweeper.IS_FIRST_CLICK:
            self.insert_mines(clicked_button.number)
            MineSweeper.IS_FIRST_CLICK = False

        if MineSweeper.IS_GAME_OVER:
            return

        if clicked_button.is_mine:
            clicked_button.config(text='*', bg='gray', disabledforeground=clicked_button.color)
            clicked_button.is_open = True
            self.game_over()
        else:
            if clicked_button.mine_around != 0:
                clicked_button.is_open = True
                clicked_button.config(text=clicked_button.mine_around, bg='gray',
                                      disabledforeground=clicked_button.color)
            else:
                # clicked_button.config(text='', disabledforeground=clicked_button.color)
                self.bfs(clicked_button)
        clicked_button.config(state='disabled')

    # выбор мин: (кнопки в масс) - (перемешать) - (взять первуе Н штук) - (список мин)
    def insert_mines(self, clicked_button_numbers):  # обозначаем кнопки минами
        def get_mines_places():  # индексы мин
            indexes = list(range(1, MineSweeper.COLUMNS * MineSweeper.ROW + 1))
            indexes.remove(clicked_button_numbers)
            shuffle(indexes)
            return indexes[:MineSweeper.MINES]

        index_mines = get_mines_places()
        for row_button in self.buttons:
            for button in row_button:
                if button.number in index_mines:
                    button.is_mine = True
        self.counting_mines()

    def count_mines_around(self, button):  # ищем мины вокруг
        count_mines = {'mines': [], 'not_mines': []}
        x, y = button.x, button.y
        for _x in [-1, 0, 1]:
            for _y in [-1, 0, 1]:
                if MineSweeper.ROW > _x + x >= 0 and MineSweeper.COLUMNS > _y + y >= 0:
                    if self.buttons[_x + x][_y + y].is_mine:
                        count_mines['mines'].append([_x, _y])
                    else:
                        count_mines['not_mines'].append([_x, _y])
        return count_mines

    def counting_mines(self):  # помечаем поля без мин количеством мин вокруг
        for row_button in self.buttons:
            for button in row_button:
                if not button.is_mine:
                    button.mine_around = len(self.count_mines_around(button)['mines'])
                    button.foreground()

    def reload(self):  # рестарт игры
        [child.destroy() for child in self.window.winfo_children()]
        self.__init__()
        self.create_widgets()
        MineSweeper.IS_FIRST_CLICK = True
        MineSweeper.IS_GAME_OVER = False

    def criate_settings_window(self):  # окно настроек (опции)
        win_settings = tk.Toplevel(self.window)

        win_settings.wm_title("Настройки")

        tk.Label(win_settings, text='Количество строк').grid(row=0, column=0)
        row_entry = tk.Entry(win_settings)
        row_entry.insert(0, str(MineSweeper.ROW))
        row_entry.grid(row=0, column=1, padx=20, pady=20)

        tk.Label(win_settings, text='Количество колонок').grid(row=1, column=0)
        column_entry = tk.Entry(win_settings)
        column_entry.insert(0, str(MineSweeper.COLUMNS))
        column_entry.grid(row=1, column=1, padx=20, pady=20)

        tk.Label(win_settings, text='Количество мин').grid(row=2, column=0)
        mines_entry = tk.Entry(win_settings)
        mines_entry.insert(0, str(MineSweeper.MINES))
        mines_entry.grid(row=2, column=1, padx=20, pady=20)

        save_btn = tk.Button(win_settings, text='Применить',
                             command=lambda: self.change_settings(row_entry, column_entry, mines_entry))

        save_btn.grid(row=3, column=0, columnspan=2, padx=20, pady=20)

    def change_settings(self, row, column, mines):  # обновление данных окна настроек
        try:
            int(row.get()), int(column.get()), int(mines.get())
        except ValueError:
            showerror('ошибка', 'введен некорркектный символ')
        MineSweeper.ROW = int(row.get())
        MineSweeper.COLUMNS = int(column.get())
        MineSweeper.MINES = int(mines.get())
        self.reload()

    def create_widgets(self):  # создание меню с выподающи списком команд
        menubar = tk.Menu(self.window)
        self.window.config(menu=menubar)

        settings_menu = tk.Menu(menubar, tearoff=0)
        settings_menu.add_command(label='играть', command=self.reload)
        settings_menu.add_command(label='настройки', command=self.criate_settings_window)
        settings_menu.add_command(label='выход', command=self.window.destroy)
        menubar.add_cascade(label='опции', menu=settings_menu)

        for i in range(MineSweeper.ROW):
            for j in range(MineSweeper.COLUMNS):
                btn = self.buttons[i][j]
                btn.grid(row=i, column=j, stick='NWES')

    def start(self):
        self.create_widgets()
        MineSweeper.window.mainloop()
