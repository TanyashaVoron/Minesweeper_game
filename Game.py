import tkinter as tk
from tkinter.messagebox import showinfo, showerror
from Button import MyButton
from Fields.Field import Field
from Fields.SphericalField import SphericalField


class MineSweeper:
    window = tk.Tk()  # основное окно игры
    IS_GAME_OVER = False  # флаг конца игры
    IS_FIRST_CLICK = True  # флаг первого клика игры

    def __init__(self):
        self.field = Field()
        self.window.wm_title('Sapper')

        count = 1
        for i in range(self.field.row):
            temp = []
            for j in range(self.field.columns):
                btn = MyButton(MineSweeper.window, x=i, y=j, number=count)
                btn.config(command=lambda button=btn: self.left_click(button))  # обработка нажатия левой кнопки мыши
                btn.bind("<Button-3>", self.right_click)  # обработка нажатия правой кнопки мыши
                temp.append(btn)
                count += 1
            self.field.buttons.append(temp)

    def right_click(self, event):
        """
        Oбработка щелчка правой кнопки мыши (постановка флажка)
        """
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

    def left_click(self, clicked_button: MyButton):
        """
        реакция на нажатие кнопки.
        Почему сюда, а не в кнопку?
        тк при нажатии реакция должна проходить не только на саму кнопку
        но еще и на соседние(если они пустые)
        :param clicked_button:
        """

        if MineSweeper.IS_FIRST_CLICK:
            self.field.insert_mines(clicked_button.number)
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
                self.field.bfs(clicked_button)
        clicked_button.config(state='disabled')
        if self.field.not_mines():
            self.game_win()

    def reload(self):
        """
        рестарт игры
        """
        [child.destroy() for child in self.window.winfo_children()]
        self.__init__()
        self.create_widgets()
        MineSweeper.IS_FIRST_CLICK = True
        MineSweeper.IS_GAME_OVER = False

    def game_over(self):
        """
        обработка проигрыша в игре
        """
        MineSweeper.IS_GAME_OVER = True
        showinfo('Game over', 'Вы проиграли(')
        self.field.restart_field()

    def game_win(self):
        """
        обработка победы в игре
        """
        MineSweeper.IS_GAME_OVER = True
        showinfo('Game over', 'Вы победили!')
        self.field.restart_field()

    def create_settings_window(self):
        """
        окно настроек (опции)
        """
        win_settings = tk.Toplevel(self.window)

        win_settings.wm_title("Настройки")

        tk.Label(win_settings, text='''Поле:
        1) стандартное
        2) сферическое''').grid(row=0, column=0)
        field = tk.Entry(win_settings)
        field.insert(0, '1')
        field.grid(row=0, column=1, padx=20, pady=20)

        tk.Label(win_settings, text='Количество строк').grid(row=0, column=0)
        row_entry = tk.Entry(win_settings)
        row_entry.insert(0, str(self.field.row))
        row_entry.grid(row=1, column=1, padx=20, pady=20)

        tk.Label(win_settings, text='Количество колонок').grid(row=1, column=0)
        column_entry = tk.Entry(win_settings)
        column_entry.insert(0, str(self.field.columns))
        column_entry.grid(row=2, column=1, padx=20, pady=20)

        tk.Label(win_settings, text='Количество мин').grid(row=2, column=0)
        mines_entry = tk.Entry(win_settings)
        mines_entry.insert(0, str(self.field.mines))
        mines_entry.grid(row=3, column=1, padx=20, pady=20)

        save_btn = tk.Button(win_settings, text='Применить',
                             command=lambda: self.change_settings(row_entry, column_entry, mines_entry, field))
        save_btn.grid(row=4, column=0, columnspan=2, padx=20, pady=20)

    def change_settings(self, row, column, mines, field):
        """
        обновление данных окна настроек
        """
        try:
            int(row.get()), int(column.get()), int(mines.get()), int(field.get())
        except ValueError:
            showerror('ошибка', 'введен некорркектный символ')
        self.field.row = int(row.get())
        self.field.columns = int(column.get())
        self.field.mines = int(mines.get())
        fil = int(field.get())
        if fil == 1:
            self.field = Field()
        elif fil == 2:
            self.field = SphericalField()
        else:
            showerror('ошибка', 'введен некорркектный символ')
        self.reload()

    def create_widgets(self):
        """
        создание понельки меню
        """
        menubar = tk.Menu(self.window)
        self.window.config(menu=menubar)

        settings_menu = tk.Menu(menubar, tearoff=0)
        settings_menu.add_command(label='играть', command=self.reload)
        settings_menu.add_command(label='настройки', command=self.create_settings_window)
        settings_menu.add_command(label='выход', command=self.window.destroy)
        menubar.add_cascade(label='опции', menu=settings_menu)

        for i in range(self.field.row):
            for j in range(self.field.columns):
                btn = self.field.buttons[i][j]
                btn.grid(row=i, column=j, stick='NWES')

    def start(self):
        self.create_widgets()
        MineSweeper.window.mainloop()
